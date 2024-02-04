from fastapi.testclient import TestClient
from .test_database import client
from .main import app
from . import schemas
import json
from . config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .database import get_db,Base
from .main import app
import pytest
from jose import jwt
from .test_database import client, session


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db =TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
# client = TestClient(app)




def test_create_user(client):
    res = client.post("/user",json={"email":"jons@gmail.com","password":"password"})
    # new_user = schemas.UserOut(**res.json())
    # assert new_user.email == "jon5@gmail.com"
    # print(f'res:{res}')
    # print(res.json())
    assert res.json().get("email") == "jons@gmail.com"
    assert res.status_code == 201

def test_root(client):
    res = client.get("/")
    print(res)
    print(res.json())
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World"

@pytest.fixture()
def create_user(client):
    user = {"email":"jons@gmail.com","password":"password"}
    res = client.post("/user",json=user)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user["password"]
    return new_user


def test_login_user(client,create_user):
    res = client.post(
        "/login", data={"username":create_user["email"],"password":create_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == create_user.get("id")
    print(res.json())
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('jons@gmail.com', 'password', 200),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password', 422)
])
def test_incorrect_login(client,create_user, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
