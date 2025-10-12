import logging
import sys

from flask import Flask


def configure_logging(app: Flask):
    """
    Configure unified logging for Flask when running under Gunicorn (or standalone).
    Logs are written to stdout/stderr so that Docker can capture them.
    """

    # Determine log level
    env = app.config.get("FLASK_ENV", "production")
    log_level = logging.DEBUG if env == "development" else logging.INFO

    # Remove default Flask handlers to avoid duplicates
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)

    # Detect if running under Gunicorn
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    if gunicorn_error_logger.handlers:
        # If running under Gunicorn, reuse its handlers
        app.logger.handlers = gunicorn_error_logger.handlers
        app.logger.setLevel(gunicorn_error_logger.level)
    else:
        # Otherwise, configure a clean stream handler to stdout
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter(
            "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        ))
        stream_handler.setLevel(log_level)
        app.logger.addHandler(stream_handler)
        app.logger.setLevel(log_level)

    # Align the Werkzeug (Flask server) logger
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(log_level)
    if not werkzeug_logger.handlers:
        werkzeug_logger.addHandler(logging.StreamHandler(sys.stdout))

    app.logger.info(
        f"Logging configured for environment: {env.upper()} (level: {logging.getLevelName(log_level)})"
    )
