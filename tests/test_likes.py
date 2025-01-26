import pytest
from app.models.vote_model import VoteModel


@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = VoteModel(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/likes/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 200


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/likes/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 400


def test_vote_unauthorized_user(client, test_posts):
    res = client.post(
        "/likes/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401