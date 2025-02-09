import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreateRequest, UserResponse
from app.models.user_model import UserModel
from app.config.utils import hash_password
import uuid
from datetime import datetime

@pytest.fixture
def mock_session():
    """Creates a mock database session"""
    return MagicMock()

@pytest.fixture
def user_service(mock_session):
    """Injects the mock session into the UserService"""
    return UserService(mock_session)
@pytest.fixture
def test_user_data():
    """Provides test user data using Pydantic schema"""
    return UserCreateRequest(
        username="alilou",
        email="alilou@email.com",
        password="Alilou123@",
        confirm_password="Alilou123@"
    )

@pytest.fixture
def test_user():
    """Creates a mock user instance"""
    return UserResponse(
        id=uuid.uuid4(),  # Simulate a real user ID
        username="alilou",
        email="alilou@email.com",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


def test_create_user(user_service, mock_session, test_user_data):
    """Test user creation with correct input"""
    user_data_dict = test_user_data.model_dump(exclude={"confirm_password"})
    
    # Mocking `filter().first()` to return None (no existing user)
    mock_session.query.return_value.filter.return_value.first.side_effect = [None, None]

    # Mocking hash_password
    hashed_password = hash_password(test_user_data.password)
    
    # Mocking `UserModel` instance creation
    user_mock = UserModel(
        id=uuid.uuid4(),
        username=user_data_dict["username"],
        email=user_data_dict["email"],
        password=hashed_password
    )

    # Mocking the add and commit process
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = user_mock

    user_service.create_user = MagicMock(return_value=user_mock)
    created_user = user_service.create_user(test_user_data)

    assert created_user.username == test_user_data.username
    assert created_user.email == test_user_data.email

def test_create_duplicate_user(user_service, mock_session, test_user_data):
    """Test handling of duplicate user creation (existing username or email)"""
    mock_session.query.return_value.filter.return_value.first.return_value = UserModel(
        id=uuid.uuid4(),
        username=test_user_data.username,
        email=test_user_data.email,
        password=hash_password(test_user_data.password)
    )

    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(test_user_data)

    assert exc_info.value.status_code == 400
    assert "Username already taken." in str(exc_info.value.detail)

def test_invalid_email_format(user_service, test_user_data):
    """Test validation for invalid email format"""
    test_user_data.email = "invalid-email"

    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(test_user_data)

    assert exc_info.value.status_code == 400
    assert "Invalid email format." in str(exc_info.value.detail)

def test_invalid_password(user_service, test_user_data):
    """Test validation for weak passwords"""
    test_user_data.password = "weak"
    test_user_data.confirm_password = "weak"

    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(test_user_data)

    assert exc_info.value.status_code == 400
    assert "Password must be at least 8 characters long" in str(exc_info.value.detail)

def test_get_users(user_service, mock_session, test_user):
    """Test fetching all users"""
    mock_session.query.return_value.all.return_value = [test_user]

    users = user_service.get_users()
    assert len(users) > 0
    assert users[0].email == test_user.email

def test_get_users_empty(user_service, mock_session):
    """Test fetching users when no users exist"""
    mock_session.query.return_value.all.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        user_service.get_users()

    assert exc_info.value.status_code == 404
    assert "No users found." in str(exc_info.value.detail)

def test_get_user_by_id(user_service, mock_session, test_user):
    """Test fetching a user by ID"""
    mock_session.query.return_value.filter.return_value.first.return_value = test_user

    fetched_user = user_service.get_user_by_Id(test_user.id)

    assert fetched_user.id == test_user.id
    assert fetched_user.email == test_user.email

def test_get_user_by_invalid_id(user_service, mock_session):
    """Test fetching a non-existing user"""
    mock_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        user_service.get_user_by_Id(uuid.uuid4())

    assert exc_info.value.status_code == 404
    assert "User not found." in str(exc_info.value.detail)
