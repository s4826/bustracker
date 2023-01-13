import os
from dotenv import load_dotenv

load_dotenv(override=True)

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_SAMESITE = 'Lax'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(base_dir, 'db/data.sqlite')
    MAIL_USERNAME = 'test@test.com'
    MAIL_PASSWORD = 'test'
    MAIL_SERVER = '0.0.0.0'
    MAIL_PORT = '1025'
    MAIL_FROM = 'test@test.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False


class TestConfig(DevelopmentConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(base_dir, 'db/test.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}
