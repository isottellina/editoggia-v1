# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Mon May  4 01:42:51 2020 (+0200)
# Last-Updated: Sat May  9 19:16:35 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Blueprint

users = Blueprint('users',
                  __name__,
                  template_folder='templates',
                  static_folder='static')

from . import models, views, admin
