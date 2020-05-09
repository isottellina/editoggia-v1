# forms.py --- 
# 
# Filename: forms.py
# Author: Louise <louise>
# Created: Tue May  5 22:08:39 2020 (+0200)
# Last-Updated: Sat May  9 23:43:39 2020 (+0200)
#           By: Louise <louise>
# 
from flask_wtf import FlaskForm
from flask_babel import gettext
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired

from app.users.models import User

class LoginForm(FlaskForm):
    username = TextField(gettext('Username'), validators=[DataRequired()])
    password = PasswordField(gettext('Password'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()

        if not self.user:
            self.username.errors.append(gettext('Unknown username'))
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append(gettext('Invalid password'))
            return False

        return True
