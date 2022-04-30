# views.py ---
#
# Filename: views.py
# Author: Louise <louise>
# Created: Tue May  5 02:33:30 2020 (+0200)
# Last-Updated: Tue Jul  7 19:05:42 2020 (+0200)
#           By: Louise <louise>
#
from datetime import datetime

from flask import flash, redirect, render_template, request, url_for
from flask_babelex import gettext
from flask_login import login_required, login_user, logout_user

from editoggia.auth import auth
from editoggia.auth.forms import LoginForm
from editoggia.extensions import lm
from editoggia.models import User
from editoggia.user.forms import SignupUserForm


@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupUserForm()
    if form.validate_on_submit():
        user = User.create(
            username=form.data["username"],
            name=form.data["name"],
            email=form.data["email"],
            password=form.data["password"],
            last_login_at=datetime.utcnow(),
            last_login_ip=request.remote_addr,
        )

        flash(
            gettext("Signed-up user {username}.".format(username=user.username)),
            "success",
        )

        login_user(user)
        return redirect(url_for("home.index"))
    return render_template("auth/register.jinja2", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)

        # set tracking info
        form.user.update(
            last_login_at=datetime.utcnow(), last_login_ip=request.remote_addr
        )

        flash(
            gettext(
                "You were logged in as {username}".format(username=form.user.username),
            ),
            "success",
        )
        return redirect(url_for("home.index"))
    return render_template("auth/login.jinja2", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash(gettext("You were logged out"), "success")
    return redirect(url_for("home.index"))
