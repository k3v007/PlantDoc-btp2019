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
    # Databse
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Image-Upload
    UPLOADED_IMAGES_DEST = os.path.join("app", "static", "images")


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class TestingConfig(Config):
    TESTING = True
