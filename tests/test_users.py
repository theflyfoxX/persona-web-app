import pytest
from app.schemas.user_schema import UserCreateRequest
from app.services.oauth2_service import create_access_token
from app.services.user_service import UserService

@pytest.fixture
def test_user(client):
    """
    Fixture to create a test user with valid fields.
    """
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "Test123@",
        "confirm_password": "Test123@"
    }
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    new_user["id"] = str(new_user["id"])  # Convert UUID to string if needed
    return new_user


@pytest.fixture
def unauthorized_test_user(client):
    """
    Fixture to create an unauthorized test user.
    """
    user_data = {
        "username": "unauthorized_user",
        "email": "unauthorized@example.com",
        "password": "Unauthorized123@",
        "confirm_password": "Unauthorized123@"
    }
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    """
    Generate a token for the test user.
    """
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    """
    Return an authorized test client with the token.
    """
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

