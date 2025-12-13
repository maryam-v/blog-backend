from flask import Blueprint, request, jsonify
from ..extensions import db
from ..services.profile_service import get_or_create_profile

profile_bp = Blueprint("profile", __name__)

@profile_bp.get("/profile")
def get_profile():
    profile = get_or_create_profile()
    return jsonify(profile.to_dict())

@profile_bp.put("/profile")
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