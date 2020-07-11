# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Sat Jul 11 21:12:34 2020 (+0200)
# Last-Updated: Sat Jul 11 21:13:02 2020 (+0200)
#           By: Louise <louise>
# 
"""
The blueprint managing the moderation aspect.
"""
from flask import Blueprint

moderation = Blueprint('moderation', __name__)

import editoggia.moderation.views
