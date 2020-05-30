# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Mon May  4 01:59:58 2020 (+0200)
# Last-Updated: Sat May 30 15:18:45 2020 (+0200)
#           By: Louise <louise>
#
from datetime import date, datetime, timedelta, timezone

from flask import abort, render_template, flash
from flask import redirect, url_for
from flask_login import current_user, login_required
from flask_babel import gettext

from editoggia.database import db
from editoggia.user import user
from editoggia.user.forms import EditUserForm

from editoggia.models import User

def get_profile_info(username):
    user = db.session.query(User).filter(User.username == username) \
                                 .first_or_404()

    # If user is the logged-in one, profile is editable
    editable = user == current_user

    # We have to calculate the age here since it's kinda bothersome
    # to do it in the template.
    age = None
    if user.birthdate:
        age = (date.today() - user.birthdate) // timedelta(days=365.2425)

    return user, editable, age

@user.route('/<username>')
def profile(username):
    """
    Prints the profile of someone.
    This returns the same thing as profile_stories,
    but has a different URL so the default tab can
    be changed easily.
    """
    return profile_stories(username)

@user.route('/<username>/stories')
def profile_stories(username):
    """
    Prints the profile of someone, with the stories
    tab opened.
    """
    user, editable, age = get_profile_info(username)
    
    return render_template('user/profile.jinja2',
                           user=user,
                           age=age,
                           mode='stories',
                           editable=editable)

@user.route('/<username>/liked')
def profile_liked(username):
    """
    Prints the profile of someone, with the liked
    stories tab opened.
    """
    user, editable, age = get_profile_info(username)
    
    return render_template('user/profile.jinja2',
                           user=user,
                           age=age,
                           mode='liked',
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
    return render_template('user/edit_profile.jinja2',
                           form=form)
