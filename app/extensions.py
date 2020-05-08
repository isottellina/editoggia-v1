# extensions.py --- 
# 
# Filename: extensions.py
# Author: Louise <louise>
# Created: Sat May  2 06:11:47 2020 (+0200)
# Last-Updated: Sat May  9 00:31:07 2020 (+0200)
#           By: Louise <louise>
# 
"""
Create all extension objects. They are then initialized
with the app in the app factory.
"""
from flask_babel import Babel
from flask_admin import Admin
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

babel = Babel()
admin = Admin()
lm = LoginManager()
bcrypt = Bcrypt()
