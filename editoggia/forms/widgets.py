# widgets.py --- 
# 
# Filename: widgets.py
# Author: Louise <louise>
# Created: Sat Jun  6 16:50:00 2020 (+0200)
# Last-Updated: Sat Jun  6 17:32:13 2020 (+0200)
#           By: Louise <louise>
#
"""
Widgets for the fields defined in fields.py
"""

from wtforms import widgets

class Select2Widget(widgets.Select):
    """
    Select2 select widget.
    select2 must be imported.    
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', u'select2')

        allow_blank = getattr(field, 'allow_blank', False)
        if allow_blank and not self.multiple:
            kwargs['data-allow-blank'] = u'1'

        return super().__call__(field, **kwargs)
