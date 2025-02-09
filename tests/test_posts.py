import pytest
import uuid
from unittest.mock import MagicMock
from fastapi import HTTPException
from datetime import datetime
from app.services.post_service import PostService
from app.schemas.post_schema import PostCreateRequest, PostResponse
from app.models.post_model import PostModel

@pytest.fixture
def mock_session():
    """Creates a mock database session"""
    return MagicMock()

@pytest.fixture
def post_service(mock_session):
    """Injects the mock session into the PostService"""
    return PostService(mock_session)

@pytest.fixture
def test_post_data():
    """Provides test post data using Pydantic schema"""
    return PostCreateRequest(
        title="My First Post",
        content="This is my first test post!"
    )

@pytest.fixture
def test_post():
    """Creates a mock post instance"""
    return PostResponse(
        id=uuid.uuid4(),
        title="My First Post",
        content="This is my first test post!",
        user_id=uuid.uuid4(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

def test_create_post(post_service, mock_session, test_post_data):
    """Test post creation with valid input"""
    post_data_dict = test_post_data.model_dump()

    # Mock PostModel instance creation
    post_mock = PostModel(
        id=uuid.uuid4(),
        title=post_data_dict["title"],
        content=post_data_dict["content"],
        user_id=uuid.uuid4()
    )

    # Mock database interactions
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = post_mock

    # Execute create_post
    post_service.create_post = MagicMock(return_value=post_mock)
    created_post = post_service.create_post(test_post_data, user_id=uuid.uuid4())

    assert created_post.title == test_post_data.title
    assert created_post.content == test_post_data.content

def test_get_posts(post_service, mock_session, test_post):
    """Test retrieving posts"""
    mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = [test_post]

    posts = post_service.get_posts(skip=0, limit=10)
    assert len(posts) > 0
    assert posts[0].title == test_post.title

def test_get_posts_empty(post_service, mock_session):
    """Test retrieving posts when no posts exist"""
    mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        post_service.get_posts()

    assert exc_info.value.status_code == 404
    assert "No posts found." in str(exc_info.value.detail)

def test_get_post_by_id(post_service, mock_session, test_post):
    """Test retrieving a post by ID"""
    mock_session.query.return_value.filter.return_value.first.return_value = test_post

    fetched_post = post_service.get_post_by_id(test_post.id)
    assert fetched_post.id == test_post.id
    assert fetched_post.title == test_post.title

def test_get_post_by_invalid_id(post_service, mock_session):
    """Test retrieving a non-existent post"""
    mock_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        post_service.get_post_by_id(uuid.uuid4())

    assert exc_info.value.status_code == 404
    assert "Post not found." in str(exc_info.value.detail)

def test_update_post(post_service, mock_session, test_post):
    """Test updating an existing post"""
    updated_data = PostCreateRequest(
        title="Updated Post Title",
        content="Updated content"
    )

    mock_session.query.return_value.filter.return_value.first.return_value = test_post

    # Execute update_post
    updated_post = post_service.update_post(test_post.id, updated_data, test_post.user_id)

    assert updated_post.title == updated_data.title
    assert updated_post.content == updated_data.content

def test_update_post_unauthorized(post_service, mock_session, test_post):
    """Test updating a post when user is not the owner"""
    different_user_id = uuid.uuid4()
    updated_data = PostCreateRequest(title="New Title", content="New content")

    mock_session.query.return_value.filter.return_value.first.return_value = test_post

    with pytest.raises(HTTPException) as exc_info:
        post_service.update_post(test_post.id, updated_data, different_user_id)

    assert exc_info.value.status_code == 403
    assert "You are not authorized to update this post." in str(exc_info.value.detail)

def test_delete_post(post_service, mock_session, test_post):
    """Test deleting a post"""
    mock_session.query.return_value.filter.return_value.first.return_value = test_post

    response = post_service.delete_post(test_post.id, test_post.user_id)

    assert response == {"message": "Post deleted successfully"}

def test_delete_post_unauthorized(post_service, mock_session, test_post):
    """Test deleting a post when user is not the owner"""
    different_user_id = uuid.uuid4()

    mock_session.query.return_value.filter.return_value.first.return_value = test_post

    with pytest.raises(HTTPException) as exc_info:
        post_service.delete_post(test_post.id, different_user_id)

    assert exc_info.value.status_code == 403
    assert "You are not authorized to delete this post." in str(exc_info.value.detail)
