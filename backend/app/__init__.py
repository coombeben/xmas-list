import os

from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import CONFIG_MAP, ProductionConfig
from .extensions import db, cors
from .errors import register_error_handlers
from .logging_setup import configure_logging
from .models import Session
from .routes import register_blueprint
from .routes.auth import validate_token


def create_app():
    # Init app
    app = Flask(__name__)
    env_name = os.environ.get('FLASK_ENV', 'production')
    config_class = CONFIG_MAP.get(env_name, ProductionConfig)
    app.config.from_object(config_class)

    configure_logging(app)

    if env_name not in CONFIG_MAP:
        app.logger.warning(f'Environment {env_name} not found, using production config')

    # Init extensions
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints
    register_blueprint(app)
    register_error_handlers(app)

    # Apply proxy fixes for nginx in production
    if env_name == 'production':
        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=3, x_for=3, x_host=3, x_prefix=1)

    app.url_map.strict_slashes = False

    @app.before_request
    def require_authorisation():
        # Send CORS response
        if request.method == 'OPTIONS':
            cors_headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
            return cors_headers, 200

        # Allow unauthenticated requests to authentication route
        if request.endpoint.startswith('auth'):
            return

        token = request.headers.get('Authorization')
        if not token or not validate_token(token):
            return {'error': 'Unauthorised'}, 401

    return app
