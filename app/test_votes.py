import pytest
from . test_users import create_user
from . import schemas
from .test_post import authorized_client,client,session,token,test_posts
from . test_users import create_user
from . import models

@pytest.fixture()
def test_vote(test_posts, session, create_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=create_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201

def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409


