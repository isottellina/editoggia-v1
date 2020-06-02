# forms.py --- 
# 
# Filename: forms.py
# Author: Louise <louise>
# Created: Fri May 22 18:40:58 2020 (+0200)
# Last-Updated: Tue Jun  2 10:59:43 2020 (+0200)
#           By: Louise <louise>
# 
from flask_wtf import FlaskForm
from flask_babel import gettext
from wtforms import StringField, TextAreaField, PasswordField
from wtforms import SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length

class StoryForm(FlaskForm):
    title = StringField(
        gettext("Title"), validators=[
            DataRequired(
                message=gettext("Title can't be empty.")
            ),
            Length(
                max=255,
                message=gettext("Title must be less than 255 characters.")
            )
        ]
    )

    summary = TextAreaField(
        gettext("Summary"), validators=[
            Length(
                max=1000,
                message=gettext("Summary must be less than 1000 characters.")
            )
        ]
    )

    fandom = SelectMultipleField(gettext("Fandoms"), validate_choice=False)
    
    content = TextAreaField(
        gettext("Content", validators=[
            Length(
                min=20,
                message=gettext("Content must be at least 20 characters.")
            )
        ])
    )

class EditStoryForm(FlaskForm):
    title = StringField(
        gettext("Title"), validators=[
            DataRequired(
                message=gettext("Title can't be empty.")
            ),
            Length(
                max=255,
                message=gettext("Title must be less than 255 characters.")
            )
        ]
    )

    summary = TextAreaField(
        gettext("Summary"), validators=[
            Length(
                max=1000,
                message=gettext("Summary must be less than 1000 characters.")
            )
        ]
    )

    fandom = SelectMultipleField(gettext("Fandoms"), validate_choice=False)
