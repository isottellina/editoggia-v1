# assets.py --- 
# 
# Filename: assets.py
# Author: Louise <louise>
# Created: Sat May  2 05:38:44 2020 (+0200)
# Last-Updated: Sun May  3 06:17:51 2020 (+0200)
#           By: Louise <louise>
# 
"""
Inits all Bundle for flask-assets.
"""
from flask_assets import Bundle, Environment

css = Bundle(
    'scss/style.scss',
    output='css/style.css',
    filters='libsass',
    depends=('**/*.scss')
)

assets = Environment()
assets.register('css_all', css)
