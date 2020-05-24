# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Mon May  4 01:42:51 2020 (+0200)
# Last-Updated: Sun May 24 20:23:14 2020 (+0200)
#           By: Louise <louise>
#
from flask import Blueprint

user = Blueprint('user',
                 __name__,
                 template_folder='templates',
                 static_folder='static')

import editoggia.user.views
import editoggia.user.admin
