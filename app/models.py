from datetime import datetime, timezone
from .extensions import db

def now_utc():
    return datetime.now(timezone.utc)

class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.Text, nullable=False, default="")
    created_at = db.Column(db.DateTime, default=now_utc, nullable=False)
    updated_at = db.Column(db.DateTime, default=now_utc, onupdate=now_utc, nullable=False)

    posts = db.relationship("Post", back_populates="author", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=now_utc, nullable=False)
    updated_at = db.Column(db.DateTime, default=now_utc, onupdate=now_utc, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)
    author = db.relationship("Author", back_populates="posts")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "author": self.author.to_dict() if self.author else None,
        }
