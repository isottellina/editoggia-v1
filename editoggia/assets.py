# assets.py --- 
# 
# Filename: assets.py
# Author: Louise <louise>
# Created: Sat May  2 05:38:44 2020 (+0200)
# Last-Updated: Sun Jun 21 15:56:00 2020 (+0200)
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
    'node_modules/jquery/dist/jquery.js',
    'node_modules/bootstrap/dist/js/bootstrap.min.js',
    'node_modules/@fortawesome/fontawesome-free/js/all.js',
    output='js/output/js_all.js'
)

js_story = Bundle(
    'js/story.js',
    output='js/output/story.js'
)

js_select2 = Bundle(
    'node_modules/select2/dist/js/select2.full.min.js',
    'js/select2.js',
    output='js/output/select2.js'
)

assets = Environment()
assets.register('css_all', css)
assets.register('js_all', js)
assets.register('js_story', js_story)
assets.register('js_select2', js_select2)
