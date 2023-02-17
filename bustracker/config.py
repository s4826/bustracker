"""Config values for different development scenarios"""
import os
from dotenv import dotenv_values

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    config = dotenv_values(".env")
    SECRET_KEY = config['SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = config['SQLALCHEMY_TRACK_MODIFICATIONS']
    SESSION_TYPE = config['SESSION_TYPE']
    SESSION_COOKIE_SAMESITE = config['SESSION_COOKIE_SAMESITE']
    SESSION_FILE_DIR = config['SESSION_FILE_DIR']

class DevelopmentConfig(Config):
    config = dotenv_values(".env.dev")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(base_dir, 'db/dev.sqlite')
    MAIL_USERNAME = config['MAIL_USERNAME']
    MAIL_PASSWORD = config['MAIL_PASSWORD'] 
    MAIL_SERVER = config['MAIL_SERVER'] 
    MAIL_PORT = config['MAIL_PORT'] 
    MAIL_FROM = config['MAIL_FROM'] 
    MAIL_USE_TLS = config['MAIL_USE_TLS']
    MAIL_USE_SSL = config['MAIL_USE_SSL']


class DevelopmentConfigWithPostgres(DevelopmentConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://sean:password@localhost/bustracker'


class TestConfig(Config):
    config = dotenv_values(".env.test")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(base_dir, 'db/test.sqlite')
    MAIL_USERNAME = config['MAIL_USERNAME']
    MAIL_PASSWORD = config['MAIL_PASSWORD'] 
    MAIL_SERVER = config['MAIL_SERVER'] 
    MAIL_PORT = config['MAIL_PORT'] 
    MAIL_API_PORT = config['MAIL_API_PORT']
    MAIL_FROM = config['MAIL_FROM'] 
    MAIL_USE_TLS = config['MAIL_USE_TLS']
    MAIL_USE_SSL = config['MAIL_USE_SSL']


config = {
    'development': DevelopmentConfig,
    'postgres_config': DevelopmentConfigWithPostgres,
    'testing': TestConfig,
    'default': DevelopmentConfig
}
