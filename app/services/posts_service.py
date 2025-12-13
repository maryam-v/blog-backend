from flask import abort
from ..extensions import db
from ..models import Post
from .authors_service import get_or_create_default_author

def list_posts(page: int, limit: int):
    if page < 1:
        return {"error": "page must be >= 1"}, 400
    if limit < 1 or limit > 50:
        return {"error": "limit must be between 1 and 50"}, 400

    total = db.session.query(Post).count()
    total_pages = (total + limit - 1) // limit

    posts = (
        Post.query.order_by(Post.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "posts": [p.to_dict() for p in posts],
    }, 200

def get_post(post_id: int):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404, description="Post not found")
    return post.to_dict()

def create_post(title: str, content: str, author_id: int | None = None):
    title = (title or "").strip()
    content = (content or "").strip()

    if not title or not content:
        return {"error": "title and content are required"}, 400

    if author_id is None:
        author_id = get_or_create_default_author().id

    post = Post(title=title, content=content, author_id=author_id)
    db.session.add(post)
    db.session.commit()

    return post.to_dict(), 201

def update_post(post_id: int, title: str | None, content: str | None):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404, description="Post not found")

    if title is not None:
        post.title = (title or "").strip()
    if content is not None:
        post.content = (content or "").strip()

    if not post.title or not post.content:
        return {"error": "title and content cannot be empty"}, 400

    db.session.commit()
    return post.to_dict(), 200

def delete_post(post_id: int):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404, description="Post not found")

    db.session.delete(post)
    db.session.commit()
    return None, 204
