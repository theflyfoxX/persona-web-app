from uuid import UUID, uuid4
import uuid
import pytest
from app.services.vote_service import VoteService
from app.models.vote_model import VoteModel
from app.models.post_model import PostModel
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


@pytest.fixture()
def vote_service(session):
    """
    Fixture to initialize the VoteService with a database session.
    """
    return VoteService(session)



def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False

def test_like_post(vote_service, test_user, test_posts):
    assert is_valid_uuid(test_user["id"]), "User ID is not a valid UUID"
    assert is_valid_uuid(test_posts[3].id), "Post ID is not a valid UUID"

    result = vote_service.like_post(user_id=test_user["id"], post_id=test_posts[3].id)
    assert result == {"message": "Post liked successfully"}

def test_like_post_already_liked(vote_service, test_user, test_posts, test_vote):
    """
    Test if attempting to like an already liked post raises an error.
    """
    with pytest.raises(HTTPException) as excinfo:
        vote_service.like_post(user_id=test_user["id"], post_id=test_posts[3].id)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "You have already liked this post"


def test_unlike_post(vote_service, test_user, test_posts, test_vote):
    """
    Test if a post can be unliked successfully via the service.
    """
    result = vote_service.unlike_post(user_id=test_user["id"], post_id=test_posts[3].id)
    assert result == {"message": "Post unliked successfully"}

    # Ensure the vote was removed from the database
    vote = vote_service.db.query(VoteModel).filter_by(
        user_id=test_user["id"], post_id=test_posts[3].id
    ).first()
    assert vote is None


def test_unlike_post_not_found(vote_service, test_user, test_posts):
    """
    Test if attempting to unlike a post that has not been liked raises an error.
    """
    with pytest.raises(HTTPException) as excinfo:
        vote_service.unlike_post(user_id=test_user["id"], post_id=test_posts[3].id)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Like not found"

def test_like_post_post_not_found(vote_service, test_user):
    """
    Test if trying to like a non-existent post raises an error.
    """
    with pytest.raises(HTTPException) as excinfo:
        # Use a valid UUID format for non-existent post
        non_existent_post_id = "00000000-0000-0000-0000-000000000000"
        vote_service.like_post(user_id=test_user["id"], post_id=non_existent_post_id)
    
    assert excinfo.value.status_code == 404
    assert "Post not found" in str(excinfo.value.detail)
    
    

def test_like_post_unauthorized_user(vote_service, unauthorized_test_user, test_posts):
    """
    Test if a post can be liked successfully via the service.
    """
    result = vote_service.like_post(user_id=unauthorized_test_user["id"], post_id=test_posts[3].id)
    assert result == {"message": "Post liked successfully"}

    # Ensure the vote was added to the database
    vote = vote_service.db.query(VoteModel).filter_by(
        user_id=unauthorized_test_user["id"], post_id=test_posts[3].id
    ).first()
    assert vote is not None
    