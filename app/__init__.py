# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Sat May  2 01:21:59 2020 (+0200)
# Last-Updated: Mon May  4 01:37:12 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Flask, render_template
from config import config

# Import extensions
from app.assets import assets
from app.extensions import db, migrate, babel

# Import blueprints
from app.home import home

def create_app(config_name="default"):
    """
    The app factory. The point where everything
    begins.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_extensions(app)
    register_blueprints(app)
    
    return app

def register_extensions(app):
    """
    Register all extensions.
    """
    assets.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)

def register_blueprints(app):
    """
    Register all blueprints.
    """
    app.register_blueprint(home)
