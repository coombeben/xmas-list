import os

__all__ = ['DevelopmentConfig', 'ProductionConfig']

connection_string = f"postgresql+psycopg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@db:5432/{os.environ.get('POSTGRES_DB')}"


class Config:
    SQLALCHEMY_DATABASE_URI = connection_string


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'dev'


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PREFERRED_URL_SCHEME = 'https'
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
