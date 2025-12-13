from ..extensions import db
from ..models import Profile

def get_or_create_profile():
    """Single profile row (id=1)."""
    profile = db.session.get(Profile, 1)
    if not profile:
        profile = Profile(id=1, name="Maryam", bio="Welcome to my blog 👋")
        db.session.add(profile)
        db.session.commit()
    return profile

def get_author_dict():
    profile = get_or_create_profile()
    return {"id": profile.id, "name": profile.name}