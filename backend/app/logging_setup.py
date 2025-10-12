import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask


def configure_logging(app: Flask):
    """
    Configures logging for the Flask application.

    Args:
        app: The Flask application instance.
    """
    # Determine the log level based on the environment
    if app.config.get('FLASK_ENV') == 'development':
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # Set the log level for the root Flask logger
    app.logger.setLevel(log_level)

    # Handle file logging
    if not app.debug and not app.testing:
        # Create a 'logs' directory if it doesn't exist
        log_directory = '/home/flask/logs'
        if not os.path.exists(log_directory):
            os.mkdir(log_directory)

        # File handler for rotating logs
        file_handler = RotatingFileHandler(
            os.path.join(log_directory, 'app.log'),
            maxBytes=10240,  # 10 KB log file size before rotation
            backupCount=10
        )

        # Define the format for log entries
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(module)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)

        # Add the file handler to the application's logger
        app.logger.addHandler(file_handler)

    # 4. Ensure console logging is enabled for production
    # (Flask's default handler might be removed by some WSGI setups)
    if not app.debug:
        # Check if the logger already has a console handler to avoid duplicates
        if not any(isinstance(handler, logging.StreamHandler) for handler in app.logger.handlers):
            # Console handler
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(logging.Formatter(
                '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
            ))
            stream_handler.setLevel(log_level)
            app.logger.addHandler(stream_handler)

        # Log confirmation
        app.logger.info(f"Application startup. Log level set to: {logging.getLevelName(log_level)}")
