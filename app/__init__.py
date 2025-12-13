import os
from flask import Flask, jsonify
from .extensions import db, cors
from .routes import register_routes

def create_app():
    app = Flask(__name__)

    db_url = os.environ.get("DATABASE_URL", "sqlite:///blog.db")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    cors.init_app(app)
    db.init_app(app)

    register_routes(app)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": str(e)}), 404

    return app
