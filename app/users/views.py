# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Mon May  4 01:59:58 2020 (+0200)
# Last-Updated: Sun May 10 22:54:22 2020 (+0200)
#           By: Louise <louise>
#
from flask import abort

from app.database import db
from app.users import users
from app.users.models import User

@users.route('/<user_name>')
def profile(user_name):
    """
    Prints the profile of someone.
    """
    user = db.session.query(User).filter(User.username == user_name) \
                                 .first()

    if user is None:
        abort(404)
    return str(user)
