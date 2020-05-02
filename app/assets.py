# assets.py --- 
# 
# Filename: assets.py
# Author: Louise <louise>
# Created: Sat May  2 05:38:44 2020 (+0200)
# Last-Updated: Sat May  2 05:40:49 2020 (+0200)
#           By: Louise <louise>
# 
"""
Inits all Bundle for flask-assets.
"""
from flask_assets import Bundle, Environment

css = Bundle(
    'style.scss',
    filters='libsass',
    output='public/css/style.css'
)

assets = Environment()

assets.register('css_all', css)
