# assets.py --- 
# 
# Filename: assets.py
# Author: Louise <louise>
# Created: Sat May  2 05:38:44 2020 (+0200)
# Last-Updated: Mon May 18 20:34:11 2020 (+0200)
#           By: Louise <louise>
# 
"""
Inits all Bundle for flask-assets.
"""
from flask_assets import Bundle, Environment

css = Bundle(
    Bundle(
        'scss/style.scss',
        filters='libsass',
        output='css/compiled.css',
        depends=('**/*.scss')
    ),
    output='css/style.css'
)

js = Bundle(
    Bundle(
        'ts/menu.ts',
        filters='typescript',
        output='js/compiled.js'
    ),
    'node_modules/jquery/dist/jquery.js',
    'node_modules/bootstrap/dist/js/bootstrap.min.js',
    'node_modules/@fortawesome/fontawesome-free/js/all.js',
    output='js/scripts.js'
)

assets = Environment()
assets.register('css_all', css)
assets.register('js_all', js)
