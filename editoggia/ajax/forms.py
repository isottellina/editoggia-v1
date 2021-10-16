# input_validate.py ---
#
# Filename: input_validate.py
# Author: Louise <louise>
# Created: Thu May 28 22:00:26 2020 (+0200)
# Last-Updated: Wed Jul  8 11:46:45 2020 (+0200)
#           By: Louise <louise>
#
from flask_wtf import FlaskForm
from flask_babelex import gettext
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired


class LikeForm(FlaskForm):
    story = IntegerField(
        "story",
        validators=[DataRequired(message=gettext("The story parameter is needed."))],
    )


class CommentForm(FlaskForm):
    chapter = IntegerField(
        "chapter",
        validators=[DataRequired(message=gettext("The chapter parameter is needed."))],
    )

    content = StringField(
        "comment", validators=[DataRequired(message=gettext("Comment can't be empty."))]
    )
