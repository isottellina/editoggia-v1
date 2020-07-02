# forms.py --- 
# 
# Filename: forms.py
# Author: Louise <louise>
# Created: Sat Jun 20 14:55:00 2020 (+0200)
# Last-Updated: Thu Jul  2 19:50:19 2020 (+0200)
#           By: Louise <louise>
# 
from flask_babel import gettext

from wtforms import Form
from wtforms.fields import SelectField

from editoggia.forms.fields import Select2MultipleAutocompleteField

class SearchForm(Form):
    """
    A form for searching. We inherit from WTForm and not Flask-WTF
    because we don't want CSRF protection, since the method used
    is GET, it would prevent bookmarking and sharing of links. 
    It would also clog up the URL for nothing.
    """
    order_by = SelectField(
        gettext("Order by"),
        choices=[
            ("title", gettext("Title")),
            ("author", gettext("Author")),
            ("date_updated", gettext("Date updated")),
            ("hits", gettext("Hits")),
            ("likes", gettext("Likes"))
        ],
        default="date_updated"
    )

    included_fandom = Select2MultipleAutocompleteField(gettext("Included fandom"), model_name='Fandom')
    included_tags = Select2MultipleAutocompleteField(gettext("Included tags"), model_name='Tag')
    excluded_tags = Select2MultipleAutocompleteField(gettext("Excluded tags"), model_name='Tag')

    def populate_select2(self):
        """
        Populate the select fields, so they can be used.
        """
        self.included_fandom.choices = []
        self.included_tags.choices = []
        self.excluded_tags.choices = []
        
