import os
from flask import Flask
from .config import config
from .extensions import db, migrate, jwt, bcrypt, cors


def create_app(env=None):
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[env])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Enable CORS for all API routes
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization", "X-Custom-Header"],
            "expose_headers": ["Authorization", "X-Custom-Header"],
            "supports_credentials": True
        }
    })

    # Add custom response headers
    @app.after_request
    def add_response_headers(response):
        response.headers['Server']       = 'Werkzeug/3.1.7 Python/3.11.9'
        response.headers['X-Powered-By'] = 'Flask/3.0'
        return response

    # Register blueprints
    from .routes.auth     import auth_bp
    from .routes.posts    import posts_bp
    from .routes.upload   import upload_bp
    from .routes.comments import comments_bp
    from .routes.admin    import admin_bp

    app.register_blueprint(auth_bp,     url_prefix='/api/auth')
    app.register_blueprint(posts_bp,    url_prefix='/api/posts')
    app.register_blueprint(upload_bp,   url_prefix='/api')
    app.register_blueprint(comments_bp, url_prefix='/api/posts')
    app.register_blueprint(admin_bp,    url_prefix='/api/admin')

    # Create database tables if they don't exist
    with app.app_context():
        from .models.user    import User
        from .models.post    import Post
        from .models.comment import Comment
        db.create_all()

    return app