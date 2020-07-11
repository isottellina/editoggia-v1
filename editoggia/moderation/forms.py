# forms.py --- 
# 
# Filename: forms.py
# Author: Louise <louise>
# Created: Sat Jul 11 21:13:06 2020 (+0200)
# Last-Updated: Sat Jul 11 22:58:17 2020 (+0200)
#           By: Louise <louise>
# 
from flask_wtf import FlaskForm
from flask_babelex import gettext

from wtforms.fields import HiddenField, StringField, FieldList, FormField
from wtforms.validators import DataRequired

from editoggia.forms.fields import Select2Field

class FandomForm(FlaskForm):
    """
    A form representing only one fandom in moderation.
    """
    id = HiddenField("fandom_id", validators=[
        DataRequired()
    ])
    
    name = StringField(gettext("Fandom name"), validators=[
        DataRequired(
            message=gettext("Fandom name can't be empty.")
        )
    ])

    category = Select2Field(
        gettext("Fandom category"),
        choices=[
            ("Anime", gettext("Anime")),
            ("Books", gettext("Books")),
            ("Cartoons", gettext("Cartoons")),
            ("Movies", gettext("Movies")),
            ("TV Shows", gettext("TV Shows")),
            ("Video games", gettext("Video games")),
            ("Other", gettext("Other"))
        ]
    )

class FandomsForm(FlaskForm):
    """
    A form representing several fandoms.
    """
    fandoms = FieldList(FormField(FandomForm))

class TagForm(FlaskForm):
    """
    A form representing only one tag in moderation.
    """
    id = HiddenField("tag_id", validators=[
        DataRequired()
    ])
    
    name = StringField(gettext("Tag name"), validators=[
        DataRequired(
            message=gettext("Tag name can't be empty.")
        )
    ])

class TagsForm(FlaskForm):
    """
    A form representing several tags.
    """
    tags = FieldList(FormField(TagForm))
