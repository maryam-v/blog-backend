from flask import Blueprint, request, jsonify
from ..extensions import db
from ..services.authors_service import get_or_create_default_author

profile_bp = Blueprint("profile", __name__)

@profile_bp.get("/profile")
def get_profile():
    author = get_or_create_default_author()
    return jsonify(author.to_dict())

@profile_bp.put("/profile")
def update_profile():
    author = get_or_create_default_author()
    data = request.get_json(silent=True) or {}

    if "name" in data:
        author.name = (data["name"] or "").strip()
    if "bio" in data:
        author.bio = (data["bio"] or "").strip()

    if not author.name:
        return jsonify({"error": "name cannot be empty"}), 400

    db.session.commit()
    return jsonify(author.to_dict())
