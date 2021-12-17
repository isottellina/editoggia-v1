# fields.py ---
#
# Filename: fields.py
# Author: Louise <louise>
# Created: Sat Jun  6 16:49:03 2020 (+0200)
# Last-Updated: Wed Jul  8 11:14:44 2020 (+0200)
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

    def process_formdata(self, data):
        """
        Override this method to set choices with it. We do it because
        if we don't set the choices, they won't show up as selected.
        """
        self.choices = [(data_sgl, data_sgl) for data_sgl in data]
        Select2MultipleField.process_formdata(self, data)


class DateField(fields.DateField):
    """
    Same as the default DateField, but with a slightly different behaviour
    in process_formdata to accept an empty value.
    """

    def process_formdata(self, valuelist):
        import datetime

        date_str = " ".join(valuelist)
        if date_str:
            try:
                self.data = datetime.datetime.strptime(date_str, self.format).date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext("Not a valid date value."))
