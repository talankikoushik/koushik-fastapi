
import pytest
from app.oauth2 import create_access_token
from .test_database import session,client
from . import models
from . test_users import create_user
from . import schemas
@pytest.fixture
def token(create_user):
    return create_access_token({"user_id": create_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(create_user, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": create_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": create_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": create_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": create_user['id']
    }]

    def create_post_model(post):
        return models.posts(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    # session.add_all([models.posts(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.posts(title="2nd title", content="2nd content", owner_id=test_user['id']), models.posts(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.posts).all()
    print(posts)
    return posts

def test_get_post(authorized_client,test_posts):
    res = authorized_client.get("/post")
    print(res.json())
    assert res.status_code == 200


# def test_get_one_post_not_exist(authorized_client, test_posts):
#     res = authorized_client.get(f"/post/88888")
#     assert res.status_code == 404
#
# def test_get_one_post(authorized_client, test_posts):
#     res = authorized_client.get(f"/post/{test_posts[0].id}")
#     print(res.jsin())
#     assert res.status_code == 200

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, create_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts", json={"title": title, "content": content, "published": published})

    assert res.status_code == 200

def test_delete_post_success(authorized_client, create_user, test_posts):
    res = authorized_client.delete(
        f"/post/{test_posts[0].id}")

    assert res.status_code == 204

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())