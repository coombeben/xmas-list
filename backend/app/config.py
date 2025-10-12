import os
from typing import Literal

__all__ = ['DevelopmentConfig', 'ProductionConfig', 'CONFIG_MAP']

connection_string = f"postgresql+psycopg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@db:5432/{os.environ.get('POSTGRES_DB')}"


class BaseConfig:
    SQLALCHEMY_DATABASE_URI = connection_string
    ENV: Literal['development', 'production'] = os.environ.get('FLASK_ENV', 'production')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    CORS_ORIGINS = []


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']


class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    CORS_ORIGINS = ['https://christmas.coombe.xyz']
    PREFERRED_URL_SCHEME = 'https'
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True


CONFIG_MAP = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
