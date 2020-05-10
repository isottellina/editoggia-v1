# assets.py --- 
# 
# Filename: assets.py
# Author: Louise <louise>
# Created: Sat May  2 05:38:44 2020 (+0200)
# Last-Updated: Sun May 10 17:45:45 2020 (+0200)
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
    'node_modules/jquery/dist/jquery.js',
    'node_modules/bootstrap/dist/js/bootstrap.min.js',
    'node_modules/@fortawesome/fontawesome-free/js/all.js',
    'js/ui.js',
    output='js/scripts.js'
)

assets = Environment()
assets.register('css_all', css)
assets.register('js_all', js)
