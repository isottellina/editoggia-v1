# fields.py --- 
# 
# Filename: fields.py
# Author: Louise <louise>
# Created: Sat Jun  6 16:49:03 2020 (+0200)
# Last-Updated: Sat Jun  6 21:36:49 2020 (+0200)
#           By: Louise <louise>
#
"""
Fields to use in the forms in the blueprints.
"""
from wtforms import fields
from editoggia.forms.widgets import Select2Widget

class Select2MultipleField(fields.SelectMultipleField):
    """
    Select2 select widget.
    """
    widget = Select2Widget(multiple=True)

    def __init__(self, label=None, validators=None, coerce=str,
                 choices=None, **kwargs):
        super().__init__(
            label, validators, coerce, choices, **kwargs
        )
