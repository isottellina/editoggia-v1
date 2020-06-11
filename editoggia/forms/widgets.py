# widgets.py --- 
# 
# Filename: widgets.py
# Author: Louise <louise>
# Created: Sat Jun  6 16:50:00 2020 (+0200)
# Last-Updated: Thu Jun 11 15:59:51 2020 (+0200)
#           By: Louise <louise>
#
"""
Widgets for the fields defined in fields.py
"""
from flask import url_for
from wtforms import widgets

class Select2Widget(widgets.Select):
    """
    Select2 select widget.
    select2 must be imported.    
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', 'select2')
        kwargs['class'] = kwargs.get('class', '') + ' select2'

        # If tags is set on the field, set data-tags to true
        if getattr(field, 'tags', False):
            kwargs['data-tags'] = '1'

        # Do the same for url, which set an AJAX endpoint for
        # select2 to get its data
        if getattr(field, 'model_name', False):
            kwargs['data-ajax--delay'] = "250"
            kwargs['data-ajax--url'] = url_for('ajax.autocomplete', model_name=field.model_name)
        
        return super().__call__(field, **kwargs)
