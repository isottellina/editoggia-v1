# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Mon May  4 01:42:51 2020 (+0200)
# Last-Updated: Mon May  4 03:22:44 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Blueprint
from app.extensions import login_manager

users = Blueprint('users',
                  __name__,
                  template_folder='templates',
                  static_folder='static')

from . import models, views

@login_manager.user_loader
def load_user(user_id):
    return models.User.get(user_id)
