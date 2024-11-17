import logging

from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import DevelopmentConfig, ProductionConfig
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

def create_app():
    # Init app
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=3, x_for=3, x_host=3, x_prefix=1)
    app.url_map.strict_slashes = False
    app.config.from_object(ProductionConfig)

    # Init extensions
    cors.init_app(app)
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
