# fields.py --- 
# 
# Filename: fields.py
# Author: Louise <louise>
# Created: Sat Jun  6 16:49:03 2020 (+0200)
# Last-Updated: Fri Jul  3 13:48:57 2020 (+0200)
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

class Select2MultipleAutocompleteField(Select2MultipleField):
    """
    Select2MultipleField, but doesn't check its data.
    This allows filling the data with autocomplete.
    """
    widget = Select2Widget(multiple=True)

    def __init__(self, *args, model_name=None, **kwargs):
        self.model_name = model_name
        self.choices = []
        super().__init__(*args, **kwargs)
    
    def pre_validate(self, form):
        """
        We don't validate the data because the choices don't exist.
        """
        pass

    def process_formdata(self, data):
        """
        Override this method to set choices with it. We do it because
        if we don't set the choices, they won't show up as selected.
        """
        self.choices = [(data_sgl, data_sgl) for data_sgl in data]
        Select2MultipleField.process_formdata(self, data)
