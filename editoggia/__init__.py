# __init__.py ---
#
# Filename: __init__.py
# Author: Louise <louise>
# Created: Sat May  2 01:21:59 2020 (+0200)
# Last-Updated: Wed Jul  8 03:01:27 2020 (+0200)
#           By: Louise <louise>
#
import requests
import arrow

from flask import Flask, render_template

# Import commands
from editoggia.commands import register_commands

# Import extensions
from editoggia.admin import admin
from editoggia.assets import assets
from editoggia.extensions import babel, lm, csrf
from editoggia.database import db, migrate

# Import blueprints
from editoggia.home import home
from editoggia.auth import auth
from editoggia.user import user
from editoggia.story import story
from editoggia.browse import browse
from editoggia.ajax import ajax

# Import misc
from editoggia.bleach import Bleacher

# Import config
from .config import config

def create_app(config_name="default"):
    """
    The app factory. The point where everything
    begins.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Create bleacher
    app.bleacher = Bleacher()

    register_commands(app)
    register_jinja_env(app)
    register_errorhandlers(app)
    register_extensions(app)
    register_blueprints(app)

    return app

def register_errorhandlers(app):
    """
    Register error handlers page.
    """
    def render_error(error):
        return render_template('errors/%s.jinja2' % error.code), error.code

    for error in [
            requests.codes.BAD_REQUEST,
            requests.codes.NOT_FOUND,
            requests.codes.UNAUTHORIZED,
            requests.codes.FORBIDDEN
    ]:
        app.errorhandler(error)(render_error)

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
    csrf.init_app(app)

def register_blueprints(app):
    """
    Register all blueprints.
    """
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(story, url_prefix='/story')
    app.register_blueprint(browse, url_prefix='/browse')
    app.register_blueprint(ajax, url_prefix='/ajax')

def register_jinja_env(app):
    """
    Register functions and modules in Jinja env.
    """
    app.jinja_options['extensions'].append('jinja2.ext.do')

    app.jinja_env.globals.update({
        'arrow': arrow
    })
