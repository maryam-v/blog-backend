import json
import os
import pytest

# IMPORTANT: set DATABASE_URL BEFORE importing the app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app  # noqa: E402
from models import db  # noqa: E402


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as client:
        yield client


def test_health(client):
    res = client.get("/")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"


def test_get_posts_empty(client):
    res = client.get("/posts")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_create_post(client):
    payload = {"title": "Test Post", "content": "Hello from tests"}
    res = client.post("/posts", data=json.dumps(payload), content_type="application/json")

    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Test Post"
    assert data["content"] == "Hello from tests"
    assert "id" in data


def test_get_single_post(client):
    # Create first
    payload = {"title": "Another", "content": "Post content"}
    create_res = client.post("/posts", data=json.dumps(payload), content_type="application/json")
    post_id = create_res.get_json()["id"]

    # Fetch
    res = client.get(f"/posts/{post_id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["id"] == post_id


def test_delete_post(client):
    # Create first
    payload = {"title": "To delete", "content": "bye"}
    create_res = client.post("/posts", data=json.dumps(payload), content_type="application/json")
    post_id = create_res.get_json()["id"]

    # Delete
    res = client.delete(f"/posts/{post_id}")
    assert res.status_code == 204

    # Confirm gone
    res2 = client.get(f"/posts/{post_id}")
    assert res2.status_code == 404
