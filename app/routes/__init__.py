from .health import health_bp
from .profile import profile_bp
from .posts import posts_bp

def register_routes(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(posts_bp)