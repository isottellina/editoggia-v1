# assets.py ---
#
# Filename: assets.py
# Author: Louise <louise>
# Created: Sat May  2 05:38:44 2020 (+0200)
# Last-Updated: Thu Jul  9 14:55:12 2020 (+0200)
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

js_search = Bundle(
    'node_modules/select2/dist/js/select2.full.min.js',
    'js/search.js',
    output='js/output/search.js'
)

js_post_story = Bundle(
    'node_modules/select2/dist/js/select2.full.min.js',
    'js/post_edit_story.js',
    'js/post_story.js',
    output='js/output/post_story.js'
)

js_edit_story = Bundle(
    'node_modules/select2/dist/js/select2.full.min.js',
    'js/post_edit_story.js',
    output='js/output/edit_story.js'
)

assets = Environment()
assets.register('css_all', css)
assets.register('js_all', js)
assets.register('js_story', js_story)
assets.register('js_search', js_search)
assets.register('js_post_story', js_post_story)
assets.register('js_edit_story', js_edit_story)
