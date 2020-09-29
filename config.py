import os
basedir = os.path.abspath(os.path.dirname(__file__))

def dotify(string_with_dots):
    ### I use this, because you cannot comfortably export a string with dots as an environmental variable - therefore, for the mail server, use underscores instead of dots, and then dotify them. If your email server is mail.somewhere.com, in the environment file put export MAIL_SERVER='mail_somewhere_com', and then dotify
    return string_with_dots.replace('_','.')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or ''
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DATASHARE_MAIL_SUBJECT_PREFIX = '[DATASHARE] '
    DATASHARE_MAIL_SENDER = dotify(os.environ.get('DATASHARE_MAIL_SENDER')) or ''
    DATASHARE_ADMIN = dotify(os.environ.get('DATASHARE_ADMIN'))

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = dotify(os.environ.get('MAIL_SERVER'))
    MAIL_PORT = os.environ.get('MAIL_PORT') ## old: 465
    MAIL_USE_TLS = True ##old:False
    MAIL_USE_SSL = False ## old:True
    MAIL_USERNAME = dotify(os.environ.get('MAIL_USERNAME'))
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTNG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    # @classmethod
    # def init_app(app):
        
    MAIL_SERVER = dotify(os.environ.get('MAIL_SERVER'))
    MAIL_PORT = os.environ.get('MAIL_PORT') ## old: 465
    MAIL_USE_TLS = True ##old:False
    MAIL_USE_SSL = False ## old:True
    MAIL_USERNAME = dotify(os.environ.get('MAIL_USERNAME'))
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
    }
