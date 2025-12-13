import json
import pytest

from app import create_app
from app.extensions import db
from app.models import Profile


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()
        db.create_all()

        # seed profile (required)
        if not db.session.get(Profile, 1):
            db.session.add(Profile(id=1, name="Maryam", bio="Test profile"))
            db.session.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_health(client):
    res = client.get("/")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"


def test_get_posts_empty(client):
    res = client.get("/posts?page=1&limit=5")
    assert res.status_code == 200
    data = res.get_json()

    assert "posts" in data
    assert isinstance(data["posts"], list)
    assert len(data["posts"]) == 0


def test_create_post(client):
    payload = {"title": "Test Post", "content": "Hello from tests"}
    res = client.post("/posts", data=json.dumps(payload), content_type="application/json")

    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Test Post"
    assert data["content"] == "Hello from tests"
    assert "id" in data


def test_get_single_post(client):
    payload = {"title": "Another", "content": "Post content"}
    create_res = client.post("/posts", data=json.dumps(payload), content_type="application/json")
    post_id = create_res.get_json()["id"]

    res = client.get(f"/posts/{post_id}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["id"] == post_id


def test_delete_post(client):
    payload = {"title": "To delete", "content": "bye"}
    create_res = client.post("/posts", data=json.dumps(payload), content_type="application/json")
    post_id = create_res.get_json()["id"]

    res = client.delete(f"/posts/{post_id}")
    assert res.status_code == 204

    res2 = client.get(f"/posts/{post_id}")
    assert res2.status_code == 404
