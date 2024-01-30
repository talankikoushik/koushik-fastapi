from fastapi.testclient import TestClient
from app.main import app
import json
client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res)
    print(res.json())
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World"
