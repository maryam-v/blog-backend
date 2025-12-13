from flask import Flask, jsonify
from .extensions import db, cors
from .routes import register_routes
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.db_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    cors.init_app(app)
    db.init_app(app)
    register_routes(app)

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": str(e)}), 404

    return app
