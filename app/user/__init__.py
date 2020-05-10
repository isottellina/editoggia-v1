# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Mon May  4 01:42:51 2020 (+0200)
# Last-Updated: Mon May 11 00:04:23 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Blueprint

user = Blueprint('user',
                 __name__,
                 url_prefix='/user',
                 template_folder='templates',
                 static_folder='static')

from . import models, views, admin
