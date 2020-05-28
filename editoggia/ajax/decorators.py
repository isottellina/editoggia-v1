# decorators.py --- 
# 
# Filename: decorators.py
# Author: Louise <louise>
# Created: Thu May 28 15:58:09 2020 (+0200)
# Last-Updated: Thu May 28 16:07:24 2020 (+0200)
#           By: Louise <louise>
#
"""
Decorators to help with views in the AJAX blueprint
"""
import functools

from flask import jsonify
from flask_babel import gettext
from flask_login import current_user

def ajax_login_required(view):
    """
    Like login_required, but returns
    a JSON response.
    """
    
    @functools.wraps(view)
    def outer_view():
        if not current_user.is_authenticated:
            return jsonify(
                message=gettext("You have to be authenticated to do this.")
            ), 401
        return view()

    return outer_view
