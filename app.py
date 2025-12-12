import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import db, Post, Profile

app = Flask(__name__)
CORS(app)

db_url = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.get("/")
def health():
    return jsonify({"status": "ok", "service": "blog-backend"})

def get_or_create_profile():
    """Single profile row (id=1)."""
    profile = db.session.get(Profile, 1)
    if not profile:
        profile = Profile(id=1, name="Maryam", bio="Welcome to my blog 👋")
        db.session.add(profile)
        db.session.commit()
    return profile

with app.app_context():
    db.create_all()
    get_or_create_profile()

# ---------------- Profile endpoints ----------------

@app.get("/profile")
def get_profile():
    profile = get_or_create_profile()
    return jsonify(profile.to_dict())

@app.put("/profile")
def update_profile():
    profile = get_or_create_profile()
    data = request.get_json(silent=True) or {}

    if "name" in data:
        profile.name = (data["name"] or "").strip()
    if "bio" in data:
        profile.bio = (data["bio"] or "").strip()

    if not profile.name:
        return jsonify({"error": "name cannot be empty"}), 400

    db.session.commit()
    return jsonify(profile.to_dict())

# ---------------- Posts endpoints ----------------

@app.get("/posts")
def list_posts():
    profile = get_or_create_profile()
    author = {"id": profile.id, "name": profile.name}

    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict(author=author) for p in posts])

@app.get("/posts/<int:post_id>")
def get_post(post_id: int):
    profile = get_or_create_profile()
    author = {"id": profile.id, "name": profile.name}

    post = db.session.get(Post, post_id)
    if not post:
        abort(404, description="Post not found")
    return jsonify(post.to_dict(author=author))

@app.post("/posts")
def create_post():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()

    if not title or not content:
        return jsonify({"error": "title and content are required"}), 400

    post = Post(title=title, content=content)
    db.session.add(post)
    db.session.commit()

    profile = get_or_create_profile()
    author = {"id": profile.id, "name": profile.name}
    return jsonify(post.to_dict(author=author)), 201

@app.put("/posts/<int:post_id>")
def update_post(post_id: int):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404, description="Post not found")

    data = request.get_json(silent=True) or {}
    if "title" in data:
        post.title = (data["title"] or "").strip()
    if "content" in data:
        post.content = (data["content"] or "").strip()

    if not post.title or not post.content:
        return jsonify({"error": "title and content cannot be empty"}), 400

    db.session.commit()

    profile = get_or_create_profile()
    author = {"id": profile.id, "name": profile.name}
    return jsonify(post.to_dict(author=author))

@app.delete("/posts/<int:post_id>")
def delete_post(post_id: int):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404, description="Post not found")

    db.session.delete(post)
    db.session.commit()
    return "", 204

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e)}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)