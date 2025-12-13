from flask import Blueprint, request, jsonify
from ..services.posts_service import (
    list_posts as svc_list_posts,
    get_post as svc_get_post,
    create_post as svc_create_post,
    update_post as svc_update_post,
    delete_post as svc_delete_post,
)

posts_bp = Blueprint("posts", __name__)

@posts_bp.get("/posts")
def list_posts():
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=5, type=int)
    payload, status = svc_list_posts(page, limit)
    return jsonify(payload), status

@posts_bp.get("/posts/<int:post_id>")
def get_post(post_id: int):
    return jsonify(svc_get_post(post_id))

@posts_bp.post("/posts")
def create_post():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()
    payload, status = svc_create_post(title, content)
    return jsonify(payload), status

@posts_bp.put("/posts/<int:post_id>")
def update_post(post_id: int):
    data = request.get_json(silent=True) or {}
    title = (data["title"] or "").strip() if "title" in data else None
    content = (data["content"] or "").strip() if "content" in data else None
    payload, status = svc_update_post(post_id, title, content)
    return jsonify(payload), status

@posts_bp.delete("/posts/<int:post_id>")
def delete_post(post_id: int):
    _, status = svc_delete_post(post_id)
    return ("", status)
