# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Thu May 14 18:24:27 2020 (+0200)
# Last-Updated: Thu May 14 19:12:40 2020 (+0200)
#           By: Louise <louise>
#
"""
The blueprint managing the story aspect of the website.
Stories, fandoms, chapters, and the like.
"""
from flask import Blueprint

story = Blueprint('story',
                  __name__,
                  template_folder='templates',
                  static_folder='static')

from . import views, models
