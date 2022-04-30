# forms.py ---
#
# Filename: forms.py
# Author: Louise <louise>
# Created: Sat Jun 20 14:55:00 2020 (+0200)
# Last-Updated: Thu Jul  9 14:23:24 2020 (+0200)
#           By: Louise <louise>
#
from flask_babelex import gettext
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
            ("likes", gettext("Likes")),
        ],
        default="date_updated",
    )

    rating = SelectField(
        gettext("Rating"),
        choices=[
            (None, gettext("Any rating")),
            ("General audiences", gettext("General audiences")),
            ("Teen and up audiences", gettext("Teen and up audiences")),
            ("Mature", gettext("Mature")),
            ("Explicit", gettext("Explicit")),
        ],
        # We have to coerce the value to get the None value right
        coerce=lambda x: None if x == "None" else x,
    )

    included_fandom = Select2MultipleAutocompleteField(
        gettext("Included fandom"), model_name="Fandom"
    )
    included_tags = Select2MultipleAutocompleteField(
        gettext("Included tags"), model_name="Tag"
    )
    excluded_tags = Select2MultipleAutocompleteField(
        gettext("Excluded tags"), model_name="Tag"
    )
