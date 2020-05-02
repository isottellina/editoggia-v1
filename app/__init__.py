# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Sat May  2 01:21:59 2020 (+0200)
# Last-Updated: Sat May  2 06:14:16 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Flask, render_template
from config import config

# Import extensions
from app.assets import assets
from app.extensions import db, migrate

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_extensions(app)
    
    # Test route, for the time being
    @app.route('/')
    def index():
        return render_template("base.html")
    
    return app

def register_extensions(app):
    """
    Register all extensions.
    """
    assets.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
