# wsgi.py ---
#
# Filename: wsgi.py
# Author: Louise <louise>
# Created: Sat Jul 11 19:40:17 2020 (+0200)
# Last-Updated: Sat Jul 11 19:40:31 2020 (+0200)
#           By: Louise <louise>
#
from editoggia import create_app

app = create_app("production")
