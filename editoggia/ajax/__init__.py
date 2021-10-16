# __init__.py ---
#
# Filename: __init__.py
# Author: Louise <louise>
# Created: Thu May 28 15:03:19 2020 (+0200)
# Last-Updated: Sat Jun 27 14:21:37 2020 (+0200)
#           By: Louise <louise>
#
from flask import Blueprint

ajax = Blueprint("ajax", __name__)

import editoggia.ajax.autocomplete
