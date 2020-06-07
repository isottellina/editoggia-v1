# fields.py --- 
# 
# Filename: fields.py
# Author: Louise <louise>
# Created: Sat Jun  6 16:49:03 2020 (+0200)
# Last-Updated: Sun Jun  7 21:02:12 2020 (+0200)
#           By: Louise <louise>
#
"""
Fields to use in the forms in the blueprints.
"""
from wtforms import fields
from editoggia.forms.widgets import Select2Widget

class Select2MultipleField(fields.SelectMultipleField):
    """
    Select2 multiple select field.
    """
    widget = Select2Widget(multiple=True)

class Select2Field(fields.SelectField):
    """
    Select2 select field.
    """
    widget = Select2Widget()

class Select2MultipleTagsField(Select2MultipleField):
    """
    Select2MultipleField, but doesn't check its data.
    That allows to create the tags (or fandoms necessary).
    """
    widget = Select2Widget(multiple=True)
    tags = True
    
    def pre_validate(self, form):
        pass
