from app import create_app
from app.extensions import db
from app.models import Profile

app = create_app()

with app.app_context():
    print("DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])

    db.create_all()

    profile = db.session.get(Profile, 1)
    if not profile:
        db.session.add(Profile(id=1, name="Maryam", bio="Welcome to my blog 👋"))
        db.session.commit()

print("DB initialized.")
