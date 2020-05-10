# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Tue May  5 02:33:30 2020 (+0200)
# Last-Updated: Mon May 11 00:57:25 2020 (+0200)
#           By: Louise <louise>
#
from flask import flash, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user
from flask_babel import gettext

from app.auth import auth
from app.extensions import lm

from app.user.models import User
from app.user.forms import SignupUserForm

from app.auth.forms import LoginForm

@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupUserForm()
    if form.validate_on_submit():
        user = User.create(
            username=form.data['username'],
            name=form.data['name'],
            email=form.data['email'],
            password=form.data['password'],
            last_login_ip=request.remote_addr,
            current_login_ip=request.remote_addr
        )

        flash(
            gettext(
                'Signed-up user {username}.'.format(
                    username=user.username
                )
            ),
            'success'
        )
        return redirect(url_for('home.index'))
    elif form.is_submitted():
        for errors in form.errors:
            for error in getattr(form, errors).errors:
                flash(error, 'warning')
    return render_template('register.jinja2', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        flash(
            gettext(
                'You were logged in as {username}'.format(
                    username=form.user.username
                ),
            ),
            'success'
        )
        return redirect(url_for('home.index'))
    elif form.is_submitted():
        for errors in form.errors:
            for error in getattr(form, errors).errors:
                flash(error, 'warning')
    return render_template('login.jinja2', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(gettext("You were logged out"), "success")
    return redirect(url_for('home.index'))
