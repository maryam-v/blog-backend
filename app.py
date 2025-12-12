import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import db, Post

app = Flask(__name__)
CORS(app)  # later you can restrict to your Vercel domain

# --- DB config: Heroku Postgres (DATABASE_URL) or local SQLite ---
db_url = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.get("/")
def health():
    return jsonify({"status": "ok", "service": "blog-backend"})

# Create tables (ok for a small technical test; later use migrations)
with app.app_context():
    db.create_all()

# --- CRUD endpoints ---

@app.get("/posts")
def list_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts])

@app.get("/posts/<int:post_id>")
def get_post(post_id: int):
    # post = Post.query.get(post_id)
    post = db.session.get(Post, post_id)
    if not post:
        abort(404, description="Post not found")
    return jsonify(post.to_dict())


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
    return jsonify(post.to_dict()), 201

@app.put("/posts/<int:post_id>")
def update_post(post_id: int):
    # post = Post.query.get(post_id)
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
    return jsonify(post.to_dict())

@app.delete("/posts/<int:post_id>")
def delete_post(post_id: int):
    # post = Post.query.get(post_id)
    post = db.session.get(Post, post_id)
    if not post:
        abort(404, description="Post not found")

    db.session.delete(post)
    db.session.commit()
    return "", 204

# nicer JSON errors
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": str(e)}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)