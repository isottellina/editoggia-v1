# editoggia.py --- 
# 
# Filename: editoggia.py
# Author: Louise <louise>
# Created: Sat May  2 01:20:11 2020 (+0200)
# Last-Updated: Sat May  2 06:11:43 2020 (+0200)
#           By: Louise <louise>
# 
import os
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
