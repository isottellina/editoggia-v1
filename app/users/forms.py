# forms.py --- 
# 
# Filename: forms.py
# Author: Louise <louise>
# Created: Tue May  5 22:09:27 2020 (+0200)
# Last-Updated: Sat May  9 01:17:47 2020 (+0200)
#           By: Louise <louise>
#
from flask_wtf import FlaskForm
from flask_babel import gettext
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.users.models import User

class UserForm(FlaskForm):
    username = StringField(
        gettext('Username'), validators=[
            DataRequired(
                message=gettext('Username must be filled.')
            ),
            Length(
                min=2,
                max=50,
                message=gettext('Username must be between 2 and 50 characters.'
                )
            )
        ]
    )
    email = StringField(
        gettext('Email'), validators=[
            Email(
                message=gettext('Email must be valid.')
            ),
            DataRequired(
                message=gettext('Email must be filled.')
            ),
            Length(
                max=128,
                message=gettext('Email must be less than 128 characters.')
            )
        ]
    )

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

class SignupUserForm(UserForm):
    name = StringField(
        gettext('Display name'), validators=[
            Length(
                max=128,
                message=gettext('Display name must be less than 128 characters.')
            )
        ]
    )
    password = PasswordField(
        gettext('Password'),
        validators=[
            DataRequired(
                message=gettext('Password must be filled.')
            ),
            EqualTo(
                'confirm',
                message=gettext('Passwords must match.')
            ),
            Length(
                min=6,
                max=50,
                message=gettext('Password must be between 6 and 50 characters.')
            )
        ]
    )
    confirm = PasswordField(
        gettext('Confirm Password'), validators=[
            DataRequired(
                message=gettext('Password must be confirmed.')
            )
        ]
    )

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append(gettext('Username already registered.'))
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append(gettext('Email already registered.'))
            return False

        self.user = user
        return True

