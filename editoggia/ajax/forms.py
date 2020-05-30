# input_validate.py --- 
# 
# Filename: input_validate.py
# Author: Louise <louise>
# Created: Thu May 28 22:00:26 2020 (+0200)
# Last-Updated: Sat May 30 15:56:39 2020 (+0200)
#           By: Louise <louise>
# 
from flask_wtf import FlaskForm
from flask_babel import gettext
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired

from editoggia.database import db
from editoggia.models import Story

class LikeForm(FlaskForm):
    story = IntegerField(
        "story", validators=[
            DataRequired(
                message=gettext("The story parameter is needed.")
            )
        ]
    )

class CommentForm(FlaskForm):
    chapter = IntegerField(
        "chapter", validators=[
            DataRequired(
                message=gettext("The chapter parameter is needed.")
            )
        ]
    )

    content = StringField(
        "comment", validators=[
            DataRequired(
                message=gettext("Comment can't be empty.")
            )
        ]
    )
