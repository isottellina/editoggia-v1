# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Tue May  5 02:33:30 2020 (+0200)
# Last-Updated: Tue May  5 22:16:23 2020 (+0200)
#           By: Louise <louise>
#
from flask import flash, render_template

from app.auth import auth
from app.extensions import lm

from app.users.forms import SignupUserForm

@lm.user_loader
def load_user(id):
    return User.get_by_id(int(id))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupUserForm()
    if form.validate_on_submit():
        user = User.create(
            username=form.data['username'],
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
        return redirect(url_for('index'))
    
    return render_template('register.html', form=form)
