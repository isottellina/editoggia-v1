# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Sat May  2 01:21:59 2020 (+0200)
# Last-Updated: Sat May  2 01:24:13 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Flask
from config import config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Test route, for the time being
    @app.route('/')
    def index():
        return 'Index page'
    
    return app
