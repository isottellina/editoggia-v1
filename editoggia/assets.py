# assets.py --- 
# 
# Filename: assets.py
# Author: Louise <louise>
# Created: Sat May  2 05:38:44 2020 (+0200)
# Last-Updated: Sat Jun  6 17:19:14 2020 (+0200)
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
        depends=('scss/**/*.scss')
    ),
    'node_modules/select2/dist/css/select2.min.css',
    output='css/style.css'
)

js = Bundle(
    'js/ui.js',
    'node_modules/jquery/dist/jquery.js',
    'node_modules/bootstrap/dist/js/bootstrap.min.js',
    'node_modules/@fortawesome/fontawesome-free/js/all.js',
    'node_modules/select2/dist/js/select2.full.min.js',
    output='js/scripts.js'
)

assets = Environment()
assets.register('css_all', css)
assets.register('js_all', js)
