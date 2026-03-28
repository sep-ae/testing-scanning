import os
from flask import Flask
from .config import config
from .extensions import db, migrate, jwt, bcrypt, cors


def create_app(env=None):
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[env])

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # CORS — sengaja misconfigured untuk target scanner TA
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": "*",
            "expose_headers": ["Authorization", "X-Custom-Header"],
            "supports_credentials": False  # harus False kalau origins: *
        }
    })

    # Tambah response headers vuln — missing security headers
    @app.after_request
    def add_vuln_headers(response):
        # Info disclosure — expose tech stack
        response.headers['Server']           = 'Werkzeug/3.1.7 Python/3.11.9'
        response.headers['X-Powered-By']     = 'Flask/3.0'

        # CORS terlalu permisif
        response.headers['Access-Control-Allow-Origin']  = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = '*'

        return response

    # Register blueprints
    from .routes.auth   import auth_bp
    from .routes.posts  import posts_bp
    from .routes.upload import upload_bp

    app.register_blueprint(auth_bp,   url_prefix='/api/auth')
    app.register_blueprint(posts_bp,  url_prefix='/api/posts')
    app.register_blueprint(upload_bp, url_prefix='/api')

    return app