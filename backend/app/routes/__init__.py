from .auth import auth_bp
from .items import items_bp
from .users import users_bp


def register_blueprint(app):
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(items_bp, url_prefix='/api/users/<int:user_id>/items')
