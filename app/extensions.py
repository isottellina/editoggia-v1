# extensions.py --- 
# 
# Filename: extensions.py
# Author: Louise <louise>
# Created: Sat May  2 06:11:47 2020 (+0200)
# Last-Updated: Mon May  4 03:19:20 2020 (+0200)
#           By: Louise <louise>
# 
"""
Create all extension objects. They are then initialized
with the app in the app factory.
"""
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_admin import Admin
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
babel = Babel()
admin = Admin()
login_manager = LoginManager()
