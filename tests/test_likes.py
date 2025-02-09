import pytest
import uuid
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.services.vote_service import VoteService
from app.schemas.vote_schema import VoteRequest, VoteResponse
from app.models.vote_model import VoteModel
from app.models.post_model import PostModel

@pytest.fixture
def mock_session():
    """Creates a mock database session"""
    return MagicMock()

@pytest.fixture
def vote_service(mock_session):
    """Injects the mock session into the VoteService"""
    return VoteService(mock_session)

@pytest.fixture
def test_post():
    """Creates a mock post instance"""
    return PostModel(
        id=uuid.uuid4(),
        title="Test Post",
        content="This is a test post",
        like_count=0  # Assuming like_count is stored in PostModel
    )

@pytest.fixture
def test_vote():
    """Creates a mock vote instance"""
    return VoteModel(
        user_id=uuid.uuid4(),
        post_id=uuid.uuid4()
    )

@pytest.fixture
def test_vote_request(test_post):
    """Provides a test vote request"""
    return VoteRequest(post_id=test_post.id)

def test_like_post(vote_service, mock_session, test_post):
    """Test liking a post"""
    user_id = uuid.uuid4()

    # Mock the post existence check
    mock_session.query.return_value.filter.return_value.first.return_value = test_post

    # Mock like existence check (user hasn't liked it yet)
    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    # Mock database commit
    mock_session.add.return_value = None
    mock_session.commit.return_value = None

    response = vote_service.like_post(user_id, test_post.id)

    assert response == {"message": "Post liked successfully"}

def test_like_post_already_liked(vote_service, mock_session, test_post, test_vote):
    """Test liking a post that has already been liked"""
    user_id = test_vote.user_id

    # Mock post existence check
    mock_session.query.return_value.filter.return_value.first.return_value = test_post

    # Mock existing like check (user has already liked)
    mock_session.query.return_value.filter_by.return_value.first.return_value = test_vote

    with pytest.raises(HTTPException) as exc_info:
        vote_service.like_post(user_id, test_post.id)

    assert exc_info.value.status_code == 400
    assert "You have already liked this post" in str(exc_info.value.detail)

def test_like_nonexistent_post(vote_service, mock_session):
    """Test liking a post that does not exist"""
    user_id = uuid.uuid4()
    post_id = uuid.uuid4()

    # Mock post existence check (post not found)
    mock_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        vote_service.like_post(user_id, post_id)

    assert exc_info.value.status_code == 404
    assert "Post not found" in str(exc_info.value.detail)

def test_unlike_post(vote_service, mock_session, test_post, test_vote):
    """Test unliking a post"""
    user_id = test_vote.user_id

    # Mock post existence check
    mock_session.query.return_value.filter.return_value.first.return_value = test_post

    # Mock like existence check (user has liked the post)
    mock_session.query.return_value.filter_by.return_value.first.return_value = test_vote

    # Mock database delete & commit
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None

    response = vote_service.unlike_post(user_id, test_post.id)

    assert response == {"message": "Post unliked successfully"}

def test_unlike_post_not_liked(vote_service, mock_session, test_post):
    """Test unliking a post that was never liked"""
    user_id = uuid.uuid4()

    # Mock post existence check
    mock_session.query.return_value.filter.return_value.first.return_value = test_post

    # Mock like existence check (user hasn't liked the post)
    mock_session.query.return_value.filter_by.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        vote_service.unlike_post(user_id, test_post.id)

    assert exc_info.value.status_code == 404
    assert "Like not found" in str(exc_info.value.detail)

def test_get_post_likes(vote_service, mock_session, test_post):
    """Test retrieving the like count for a post"""
    # Mock post existence check
    mock_session.query.return_value.filter.return_value.first.return_value = test_post

    # Mock count of likes
    mock_session.query.return_value.filter_by.return_value.count.return_value = 5

    response = vote_service.get_post_likes(test_post.id)

    assert response == {"post_id": test_post.id, "like_count": 5}

def test_get_post_likes_nonexistent_post(vote_service, mock_session):
    """Test retrieving like count for a non-existent post"""
    post_id = uuid.uuid4()

    # Mock post existence check (post not found)
    mock_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        vote_service.get_post_likes(post_id)

    assert exc_info.value.status_code == 404
    assert "Post not found" in str(exc_info.value.detail)
