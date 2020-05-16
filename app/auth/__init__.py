# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Tue May  5 02:33:01 2020 (+0200)
# Last-Updated: Sat May 16 17:39:08 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Blueprint

auth = Blueprint('auth',
                 __name__,
                 template_folder='templates')

import app.auth.views
