# forms.py ---
#
# Filename: forms.py
# Author: Louise <louise>
# Created: Tue May  5 22:09:27 2020 (+0200)
# Last-Updated: Wed Jul  8 11:49:23 2020 (+0200)
#           By: Louise <louise>
#
from flask import current_app
from flask_wtf import FlaskForm
from flask_babelex import gettext, Locale

from wtforms.fields import StringField, TextAreaField, PasswordField
from wtforms.fields import SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from editoggia.models import User
from editoggia.forms.fields import DateField


class UserForm(FlaskForm):
    username = StringField(
        gettext("Username"),
        validators=[
            DataRequired(message=gettext("Username must be filled.")),
            Length(
                min=2,
                max=50,
                message=gettext("Username must be between 2 and 50 characters."),
            ),
        ],
    )
    email = StringField(
        gettext("Email"),
        validators=[
            Email(message=gettext("Email must be valid.")),
            DataRequired(message=gettext("Email must be filled.")),
            Length(max=128, message=gettext("Email must be less than 128 characters.")),
        ],
    )

    name = StringField(
        gettext("Display name"),
        validators=[
            Length(
                max=128,
                message=gettext("Display name must be less than 128 characters."),
            )
        ],
    )

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)


class SignupUserForm(UserForm):
    password = PasswordField(
        gettext("Password"),
        validators=[
            DataRequired(message=gettext("Password must be filled.")),
            EqualTo("confirm", message=gettext("Passwords must match.")),
            Length(
                min=6,
                max=50,
                message=gettext("Password must be between 6 and 50 characters."),
            ),
        ],
    )
    confirm = PasswordField(
        gettext("Confirm Password"),
        validators=[DataRequired(message=gettext("Password must be confirmed."))],
    )

    def __init__(self, *args, **kwargs):
        UserForm.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = FlaskForm.validate(self)

        if not self.username.data.isalnum():
            self.username.errors.append(
                gettext("Username can only contain " "alphanumerical characters.")
            )
            return False

        # return this after because we might have to add the aforementioned error
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append(gettext("Username already registered."))
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append(gettext("Email already registered."))
            return False

        self.user = user
        return True


class EditUserForm(UserForm):
    gender = SelectField(
        gettext("Gender"),
        choices=[
            ("Woman", gettext("Woman")),
            ("Man", gettext("Man")),
            ("Other", gettext("Other")),
            (None, gettext("Doesn't want to say")),
        ],
        # We have to coerce the value to get the None value right
        coerce=lambda x: None if x == "None" else x,
    )

    language = SelectField(gettext("Language"))

    location = StringField()
    birthdate = DateField()
    bio = TextAreaField()

    def populate_language(self):
        """
        Populate the language choices, we have to do it
        here since we need the app context.
        """
        self.language.choices = [
            (lang, Locale.parse(lang).get_display_name(lang))
            for lang in current_app.config["ACCEPTED_LANGUAGES"]
        ]
