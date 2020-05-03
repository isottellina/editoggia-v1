# __init__.py --- 
# 
# Filename: __init__.py
# Author: Louise <louise>
# Created: Sun May  3 04:36:07 2020 (+0200)
# Last-Updated: Sun May  3 04:50:33 2020 (+0200)
#           By: Louise <louise>
# 
from flask import Blueprint
from flask import render_template

home = Blueprint('home',
                 __name__,
                 template_folder='templates',
                 static_folder='static')

@home.route('/')
def index():
    return render_template('base.html')
