from flask import abort
from ..extensions import db
from ..models import Post
from .profile_service import get_author_dict

def list_posts(page: int, limit: int):
    if page < 1:
        return {"error": "page must be >= 1"}, 400
    if limit < 1 or limit > 50:
        return {"error": "limit must be between 1 and 50"}, 400

    author = get_author_dict()

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
        "posts": [p.to_dict(author=author) for p in posts],
    }, 200

def get_post(post_id: int):
    author = get_author_dict()
    post = db.session.get(Post, post_id)
    if not post:
        abort(404, description="Post not found")
    return post.to_dict(author=author)

def create_post(title: str, content: str):
    if not title or not content:
        return {"error": "title and content are required"}, 400

    post = Post(title=title, content=content)
    db.session.add(post)
    db.session.commit()

    author = get_author_dict()
    return post.to_dict(author=author), 201

def update_post(post_id: int, title: str | None, content: str | None):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404, description="Post not found")

    if title is not None:
        post.title = title
    if content is not None:
        post.content = content

    if not post.title or not post.content:
        return {"error": "title and content cannot be empty"}, 400

    db.session.commit()

    author = get_author_dict()
    return post.to_dict(author=author), 200

def delete_post(post_id: int):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404, description="Post not found")

    db.session.delete(post)
    db.session.commit()
    return None, 204
