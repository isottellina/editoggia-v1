# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Sun May  3 04:36:07 2020 (+0200)
# Last-Updated: Sat May 16 17:38:34 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Blueprint

home = Blueprint('home',
                 __name__,
                 template_folder='templates',
                 static_folder='static')

import app.home.views
