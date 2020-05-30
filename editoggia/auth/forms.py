# forms.py --- 
# 
# Filename: forms.py
# Author: Louise <louise>
# Created: Tue May  5 22:08:39 2020 (+0200)
# Last-Updated: Sat May 30 15:20:35 2020 (+0200)
#           By: Louise <louise>
# 
from flask_wtf import FlaskForm
from flask_babel import gettext
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from editoggia.models import User

class LoginForm(FlaskForm):
    username = StringField(gettext('Username'), validators=[
        DataRequired(
            message=gettext('Username must be filled.')
        )
    ])
    password = PasswordField(gettext('Password'), validators=[
        DataRequired(
            message=gettext('Password must be filled.')
        )
    ])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        self.user = User.query.filter_by(username=self.username.data).first()

        if not self.user:
            self.username.errors.append(gettext('Unknown username.'))
            return False

        if not self.user.check_password(self.password.data):
            self.password.errors.append(gettext('Invalid password.'))
            return False

        return True
