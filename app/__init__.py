from flask import Flask, jsonify
from .config import DevelopmentConfig
from .extensions import db, cors
from .routes import register_routes
from .services.profile_service import get_or_create_profile

def create_app(config_object=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    cors.init_app(app)
    db.init_app(app)

    register_routes(app)

    with app.app_context():
        db.create_all()
        get_or_create_profile()

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": str(e)}), 404

    return app
