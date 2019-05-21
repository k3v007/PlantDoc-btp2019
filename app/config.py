import datetime
import os


class Config(object):
    # Flask App
    CSRF_ENABLED = True
    DEBUG = False
    PROPAGATE_EXCEPTIONS = True
    SECRET_KEY = os.environ['SECRET_KEY']
    TESTING = False
    THREADED = True
    APP_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
    CLIENTS_DIR_PATH = os.path.join(APP_DIR_PATH, "static", "clients")
    TEMP_DIR_PATH = os.path.join(APP_DIR_PATH, "static", "clients", "temp")
    ALLOWED_IMAGE_EXT = tuple("bmp gif jpg jpeg png".split())
    # JWT
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh", ]
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=2)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=90)
    # Databse
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    DEBUG = False
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']


class TestConfig(Config):
    TESTING = True
