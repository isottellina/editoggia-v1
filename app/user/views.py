# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Mon May  4 01:59:58 2020 (+0200)
# Last-Updated: Mon May 11 00:05:07 2020 (+0200)
#           By: Louise <louise>
#
from flask import abort, render_template
from flask_login import current_user

from app.database import db
from app.user import user
from app.user.models import User

@user.route('/<user_name>')
def profile(user_name):
    """
    Prints the profile of someone.
    """
    user = db.session.query(User).filter(User.username == user_name) \
                                 .first()

    # If user doesn't exist, 404 error.
    if user is None:
        abort(404)
    # If user is the logged-in one, profile is editable
    editable = user == current_user
    
    return render_template('profile.jinja2',
                           user=user,
                           editable=editable)
