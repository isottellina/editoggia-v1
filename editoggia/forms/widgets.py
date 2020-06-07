# widgets.py --- 
# 
# Filename: widgets.py
# Author: Louise <louise>
# Created: Sat Jun  6 16:50:00 2020 (+0200)
# Last-Updated: Sun Jun  7 21:02:01 2020 (+0200)
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
        kwargs['class'] = kwargs.get('class', '') + ' select2'

        # If tags is set on the field, set data-tags to true
        if getattr(field, 'tags', False):
            kwargs['data-tags'] = '1'
        
        return super().__call__(field, **kwargs)
