# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Tue May  5 02:33:01 2020 (+0200)
# Last-Updated: Tue May  5 02:36:09 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Blueprint

auth = Blueprint('auth',
                 __name__,
                 template_folder='templates')

from . import views
