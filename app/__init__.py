# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Sat May  2 01:21:59 2020 (+0200)
# Last-Updated: Tue May 12 22:49:36 2020 (+0200)
#           By: Louise <louise>
#
import requests
import arrow

from flask import Flask, render_template
from .config import config

# Import commands
from app.commands import register_commands

# Import extensions
from app.admin import admin
from app.assets import assets
from app.extensions import babel, lm
from app.database import db, migrate

# Import blueprints
from app.home import home
from app.auth import auth
from app.user import user

def create_app(config_name="default"):
    """
    The app factory. The point where everything
    begins.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_commands(app)
    register_errorhandlers(app)
    register_extensions(app)
    register_blueprints(app)
    register_jinja_env(app)
    
    return app

def register_errorhandlers(app):
    """
    Register error handlers page.
    """
    def render_error(e):
        return render_template('errors/%s.jinja2' % e.code), e.code
    
    for e in [
            requests.codes.INTERNAL_SERVER_ERROR,
            requests.codes.NOT_FOUND,
            requests.codes.UNAUTHORIZED,
    ]:
        app.errorhandler(e)(render_error)
        
def register_extensions(app):
    """
    Register all extensions.
    """
    assets.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)
    admin.init_app(app)
    lm.init_app(app)

def register_blueprints(app):
    """
    Register all blueprints.
    """
    app.register_blueprint(home)
    app.register_blueprint(auth)
    app.register_blueprint(user)

def register_jinja_env(app):
    """
    Register functions and modules in Jinja env.
    """
    app.jinja_env.globals.update({
        'arrow': arrow
    })
