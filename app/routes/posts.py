from flask import Blueprint, request, jsonify
from ..services.posts_service import (
    list_posts as svc_list,
    get_post as svc_get,
    create_post as svc_create,
    update_post as svc_update,
    delete_post as svc_delete,
)

posts_bp = Blueprint("posts", __name__)

@posts_bp.get("/posts")
def list_posts():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=5, type=int)
    payload, status = svc_list(page, limit)
    return jsonify(payload), status

@posts_bp.get("/posts/<int:post_id>")
def get_post(post_id: int):
    return jsonify(svc_get(post_id))

@posts_bp.post("/posts")
def create_post():
    data = request.get_json(silent=True) or {}
    payload, status = svc_create(
        data.get("title"),
        data.get("content"),
        data.get("author_id"),
    )
    return jsonify(payload), status

@posts_bp.put("/posts/<int:post_id>")
def update_post(post_id: int):
    data = request.get_json(silent=True) or {}
    payload, status = svc_update(post_id, data.get("title"), data.get("content"))
    return jsonify(payload), status

@posts_bp.delete("/posts/<int:post_id>")
def delete_post(post_id: int):
    _, status = svc_delete(post_id)
    return ("", status)