import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '@my1strealapp'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DATASHARE_MAIL_SUBJECT_PREFIX = '[DATASHARE] '
    DATASHARE_MAIL_SENDER = 'Datashare Admin <datashare@imdata.eu>'
    DATASHARE_ADMIN = os.environ.get('DATASHARE_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'mail.imdata.eu'
    MAIL_PORT = 587 ## old: 465
    MAIL_USE_TLS = True ##old:False
    MAIL_USE_SSL = False ## old:True
    MAIL_USERNAME = 'datashare@imdata.eu'
    MAIL_PASSWORD = '@my1stdatashare'
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
