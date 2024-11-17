from sqlalchemy.exc import SQLAlchemyError

def register_error_handlers(app):
    @app.errorhandler(403)
    def forbidden(error):
        return {'error': 'Forbidden'}, 403

    @app.errorhandler(400)
    def bad_request(e):
        return {'error': 'Bad Request'}, 400

    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404

    @app.errorhandler(SQLAlchemyError)
    def database_error(error):
        return {'error': 'A database error occurred'}, 500

    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal Server Error'}, 500
