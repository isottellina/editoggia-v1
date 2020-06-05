# forms.py --- 
# 
# Filename: forms.py
# Author: Louise <louise>
# Created: Fri May 22 18:40:58 2020 (+0200)
# Last-Updated: Fri Jun  5 16:17:46 2020 (+0200)
#           By: Louise <louise>
# 
from flask_wtf import FlaskForm
from flask_babel import gettext
from wtforms import StringField, TextAreaField
from wtforms import SelectField, SelectMultipleField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, NumberRange, Length

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
    
    rating = SelectField(
        gettext("Rating"),
        choices=[
            (None, gettext("Not rated")),
            ("General audiences", gettext("General audiences")),
            ("Teen and up audiences", gettext("Teen and up audiences")),
            ("Mature", gettext("Mature")),
            ("Explicit", gettext("Explicit"))
        ],
        # We have to coerce the value to get the None value right
        coerce=lambda x: None if x=="None" else x
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

class PostStoryForm(StoryForm):
    content = TextAreaField(
        gettext("Content", validators=[
            Length(
                min=20,
                message=gettext("Content must be at least 20 characters.")
            )
        ])
    )
    
class EditStoryForm(StoryForm):
    pass

class EditChapterForm(FlaskForm):
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

    nb = IntegerField(
        gettext("Chapter number"), validators=[
            DataRequired(
                message=gettext("Chapter number can't be empty.")
            ),
            NumberRange(
                min=0,
                message=gettext("Chapter number can't be less than zero.")
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

    content = TextAreaField(
        gettext("Content", validators=[
            Length(
                min=20,
                message=gettext("Content must be at least 20 characters.")
            )
        ])
    )
