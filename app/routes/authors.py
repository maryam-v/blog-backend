from flask import Blueprint, request, jsonify, abort
from ..services.authors_service import get_author, list_author_posts

authors_bp = Blueprint("authors", __name__)

@authors_bp.get("/authors/<int:author_id>")
def get_author_route(author_id: int):
    author = get_author(author_id)
    if not author:
        abort(404, description="Author not found")
    return jsonify(author.to_dict())

@authors_bp.get("/authors/<int:author_id>/posts")
def get_author_posts_route(author_id: int):
    author = get_author(author_id)
    if not author:
        abort(404, description="Author not found")

    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=5, type=int)

    payload, status = list_author_posts(author_id, page, limit)
    return jsonify(payload), status