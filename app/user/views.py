# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Mon May  4 01:59:58 2020 (+0200)
# Last-Updated: Mon May 11 17:59:59 2020 (+0200)
#           By: Louise <louise>
#
from flask import abort, render_template, flash
from flask import redirect, url_for
from flask_login import current_user, login_required
from flask_babel import gettext

from app.database import db
from app.user import user
from app.user.models import User
from app.user.forms import EditUserForm

@user.route('/<username>')
def profile(username):
    """
    Prints the profile of someone.
    """
    user = db.session.query(User).filter(User.username == username) \
                                 .first()

    # If user doesn't exist, 404 error.
    if user is None:
        abort(404)
    # If user is the logged-in one, profile is editable
    editable = user == current_user
    
    return render_template('profile.jinja2',
                           user=user,
                           editable=editable)

@user.route('/edit', methods=["GET", "POST"])
@login_required
def edit_profile():
    """
    Edit a user profile.
    """
    form = EditUserForm(obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        current_user.update()
        
        flash(
            gettext("Profile edited with success"),
            "success"
        )
        return redirect(url_for('user.profile',
                                username=current_user.username))
    return render_template('edit_profile.jinja2',
                           form=form)
