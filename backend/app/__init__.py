import logging
import os

from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import CONFIG_MAP, ProductionConfig
from .extensions import db, cors
from .routes import register_blueprint
from .models import Session
from .errors import register_error_handlers
from .routes.auth import validate_token

logging.basicConfig(
    filename='/var/log/flask.log',
    level=logging.WARNING,
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    env_name = os.environ.get('FLASK_ENV', 'production')
    try:
        config_class = CONFIG_MAP.get[env_name]
    except KeyError:
        logger.warning(f'Environment {env_name} not found, using production config')
        config_class = ProductionConfig

    # Init app
    app = Flask(__name__)

    # Apply proxy fixes for nginx in production
    if env_name == 'production':
        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=3, x_for=3, x_host=3, x_prefix=1)

    app.url_map.strict_slashes = False
    app.config.from_object(config_class)

    # Init extensions
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints
    register_blueprint(app)
    register_error_handlers(app)

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
