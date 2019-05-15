import datetime
import os


class Config(object):
    # Flask App
    CSRF_ENABLED = True
    DEBUG = False
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    TESTING = False
    THREADED = True
    # JWT
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh", ]
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=2)
    JWT_REFRESS_TOKEN_EXPIRES = datetime.timedelta(days=90)

    # Databse
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class TestConfig(Config):
    TESTING = True
