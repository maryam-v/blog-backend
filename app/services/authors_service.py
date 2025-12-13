from ..extensions import db
from ..models import Author, Post

def get_or_create_default_author():
    author = db.session.get(Author, 1)
    if not author:
        author = Author(id=1, name="Maryam", bio="Welcome to my blog 👋")
        db.session.add(author)
        db.session.commit()
    return author

def get_author(author_id: int):
    return db.session.get(Author, author_id)

def list_author_posts(author_id: int, page: int, limit: int):
    if page < 1:
        return {"error": "page must be >= 1"}, 400
    if limit < 1 or limit > 50:
        return {"error": "limit must be between 1 and 50"}, 400

    q = Post.query.filter_by(author_id=author_id).order_by(Post.created_at.desc())
    total = q.count()
    total_pages = (total + limit - 1) // limit

    posts = q.offset((page - 1) * limit).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "posts": [p.to_dict() for p in posts],
    }, 200