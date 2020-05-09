# config.py --- 
# 
# Filename: config.py
# Author: Louise <louise>
# Created: Sat May  2 01:05:35 2020 (+0200)
# Last-Updated: Sat May  9 19:48:34 2020 (+0200)
#           By: Louise <louise>
# 
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # General config
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
        'awa3&#-0xm3-g7h*rvw(=@h7@%9xd1vuo&1=&q4kja8hbvg&=j'

    # SQLAlchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # i18n and l10n options
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

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

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
