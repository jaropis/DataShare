import os
basedir = os.path.abspath(os.path.dirname(__file__))
import sys
sys.path.append(basedir)
print(basedir)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or ''
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DATASHARE_MAIL_SUBJECT_PREFIX = '[DATASHARE] '
    DATASHARE_MAIL_SENDER = ''
    DATASHARE_ADMIN = os.environ.get('DATASHARE_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = ''
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTNG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
    }
