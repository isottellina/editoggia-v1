# __init__.py ---
#
# Filename: __init__.py
# Author: Louise <louise>
# Created: Sun May  3 04:36:07 2020 (+0200)
# Last-Updated: Thu May 28 15:03:00 2020 (+0200)
#           By: Louise <louise>
#
from flask import Blueprint

home = Blueprint('home', __name__)

import editoggia.home.views
