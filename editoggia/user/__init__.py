# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Mon May  4 01:42:51 2020 (+0200)
# Last-Updated: Sun May 24 20:20:44 2020 (+0200)
#           By: Louise <louise>
#
from datetime import datetime

from flask import Blueprint, request
from flask_login import current_user

from editoggia.database import db

user = Blueprint('user',
                 __name__,
                 template_folder='templates',
                 static_folder='static')

@user.before_app_request
def register_user_request():
    if not current_user.is_anonymous:
        current_user.last_active_at = datetime.utcnow()
        current_user.last_active_ip = request.remote_addr
        db.session.commit()

import editoggia.user.views
import editoggia.user.admin
