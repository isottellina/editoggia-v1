# __init__.py ---
#
# Filename: __init__.py
# Author: Louise <louise>
# Created: Thu Jun  4 14:49:32 2020 (+0200)
# Last-Updated: Thu Jun  4 17:02:08 2020 (+0200)
#           By: Louise <louise>
#
from flask import Blueprint

browse = Blueprint("browse", __name__)

import editoggia.browse.views  # noqa
