# __init__.py ---
#
# Filename: __init__.py
# Author: Louise <louise>
# Created: Tue May  5 02:33:01 2020 (+0200)
# Last-Updated: Sun Jun 14 14:21:41 2020 (+0200)
#           By: Louise <louise>
#
from datetime import datetime

from flask import Blueprint, request
from flask_login import current_user

from editoggia.database import db

auth = Blueprint('auth', __name__)

@auth.before_app_request
def register_user_request():
    """
    If the user is connected, register the
    last time they loaded a page (now).
    """
    if not current_user.is_anonymous:
        current_user.update(
            last_active_at = datetime.utcnow(),
            last_active_ip = request.remote_addr
        )

import editoggia.auth.views
