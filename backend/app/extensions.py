"""
This module initializes and exports instances for database connection using
SQLAlchemy and Cross-Origin Resource Sharing (CORS) management with Flask-CORS.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

__all__ = ['db', 'cors']

db = SQLAlchemy()
cors = CORS()
