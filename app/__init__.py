from flask import Flask, jsonify
from .config import DevelopmentConfig
from .extensions import db, cors
from .routes import register_routes

def create_app(config_object=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)

    cors.init_app(app)
    db.init_app(app)

    register_routes(app)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": str(e)}), 404

    return app
