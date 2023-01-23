"""Config values for different development scenarios"""
import os
from dotenv import dotenv_values

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    config = dotenv_values(".env")
    SECRET_KEY = config['SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_COOKIE_SAMESITE = 'Lax'


class DevelopmentConfig(Config):
    config = dotenv_values(".env.dev")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(base_dir, 'db/data.sqlite')
    MAIL_USERNAME = config['MAIL_USERNAME']
    MAIL_PASSWORD = config['MAIL_PASSWORD'] 
    MAIL_SERVER = config['MAIL_SERVER'] 
    MAIL_PORT = config['MAIL_PORT'] 
    MAIL_FROM = config['MAIL_FROM'] 
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


class TestConfig(Config):
    config = dotenv_values(".env.test")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(base_dir, 'db/test.sqlite')
    MAIL_USERNAME = config['MAIL_USERNAME']
    MAIL_PASSWORD = config['MAIL_PASSWORD'] 
    MAIL_SERVER = config['MAIL_SERVER'] 
    MAIL_PORT = config['MAIL_PORT'] 
    MAIL_FROM = config['MAIL_FROM'] 
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}
