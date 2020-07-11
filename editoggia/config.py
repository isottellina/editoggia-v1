# config.py ---
#
# Filename: config.py
# Author: Louise <louise>
# Created: Sat May  2 01:05:35 2020 (+0200)
# Last-Updated: Sat Jul 11 20:31:35 2020 (+0200)
#           By: Louise <louise>
#
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # General config
    SECRET_KEY = os.environ.get('EDITOGGIA_SECRET_KEY') or \
        'awa3&#-0xm3-g7h*rvw(=@h7@%9xd1vuo&1=&q4kja8hbvg&=j'

    # SQLAlchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # i18n and l10n options
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"
    ACCEPTED_LANGUAGES = ["en"]

    # Flask admin
    FLASK_ADMIN_SWATCH = "journal"

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '../db.sqlite3')

    # Assets config
    ASSETS_DEBUG = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///:memory:'

class ProductionConfig(Config):
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
    POSTGRES_DB = os.environ.get('POSTGRES_DB', 'editoggia')
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
