# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Mon May  4 00:22:56 2020 (+0200)
# Last-Updated: Mon May  4 00:30:35 2020 (+0200)
#           By: Louise <louise>
#
from flask import render_template

from app.home import home

@home.route('/')
def index():
    return render_template('index.html')
