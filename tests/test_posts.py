from fastapi import HTTPException
import pytest
from app.models.post_model import PostModel
from app.schemas.post_schema import PostResponse, PostCreateRequest
from app.services.post_service import PostService



@pytest.fixture()
def post_service(session):
    """
    Fixture to initialize the VoteService with a database session.
    """
    return PostService(session)



def test_get_posts_success(post_service, test_posts):
    posts = post_service.get_posts(skip=0, limit=10)
    assert len(posts) == len(test_posts)
    assert posts[0].title == "first title"
    assert posts[1].title == "2nd title"

def test_get_posts_no_posts(post_service, session):
    session.query(PostModel).delete()  # Delete all posts from the database
    session.commit()

    with pytest.raises(HTTPException) as excinfo:
        post_service.get_posts(skip=0, limit=10)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "No posts found."

    
def test_get_posts_pagination(post_service, test_posts):
    posts = post_service.get_posts(skip=1, limit=2)
    assert len(posts) == 2
    assert posts[0].title == "2nd title"

def test_create_post_success(post_service, test_user):
    post_data = PostCreateRequest(title="New Post", content="New Content")
    new_post = post_service.create_post(post_data=post_data, user_id=test_user["id"])
    assert new_post.title == "New Post"
    assert new_post.content == "New Content"
    assert str(new_post.user_id) == test_user["id"]
    
    
def test_get_post_by_id_not_found(post_service):
    non_existent_post_id = "00000000-0000-0000-0000-000000000000"
    with pytest.raises(HTTPException) as excinfo:
        post_service.get_post_by_id(post_id=non_existent_post_id)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Post not found."


def test_get_post_by_id_invalid_uuid(post_service):
    invalid_post_id = "invalid-uuid"
    with pytest.raises(HTTPException) as exc_info:
        post_service.get_post_by_id(post_id=invalid_post_id)
    assert exc_info.value.status_code == 400
    assert "Invalid UUID format" in str(exc_info.value.detail)
    
def test_get_post_by_id_success(post_service, test_posts):
    post = post_service.get_post_by_id(post_id=str(test_posts[0].id))
    assert post.title == "first title"
    assert post.content == "first content"
    assert post.user_id == test_posts[0].user_id
    assert post.id == test_posts[0].id
    

def test_create_post_no_title(post_service, test_user):
    post_data = PostCreateRequest(title="", content="New Content")
    with pytest.raises(HTTPException) as excinfo:
        post_service.create_post(post_data=post_data, user_id=test_user["id"])
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Title and content are required."
    
    
    
def test_create_post_no_content(post_service, test_user):
    post_data = PostCreateRequest(title="New Post", content="")
    with pytest.raises(HTTPException) as excinfo:
        post_service.create_post(post_data=post_data, user_id=test_user["id"])
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Title and content are required."
    
    
def test_create_post_no_title_and_content(post_service, test_user):
    post_data = PostCreateRequest(title="", content="")
    with pytest.raises(HTTPException) as excinfo:
        post_service.create_post(post_data=post_data, user_id=test_user["id"])
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Title and content are required."
    

def test_get_posts_unauthorized(post_service, test_posts):
    """
    Test that an unauthorized user can access public posts.
    """
    posts = post_service.get_posts(skip=0, limit=10)
    assert len(posts) == len(test_posts)  
    