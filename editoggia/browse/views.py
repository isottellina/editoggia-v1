# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Thu Jun  4 16:55:50 2020 (+0200)
# Last-Updated: Fri Jun 19 18:43:59 2020 (+0200)
#           By: Louise <louise>
# 
from flask import render_template

from editoggia.browse import browse
from editoggia.database import db
from editoggia.models import FandomCategory, Fandom, Story, Tag

@browse.route('/fandoms/<category>')
def fandoms(category):
    """
    Print all fandoms in a category.
    """
    fandomcategory = db.session.query(FandomCategory) \
                               .filter(FandomCategory.name == category) \
                               .first_or_404()

    return render_template('browse/fandoms.jinja2', category=fandomcategory)

@browse.route('/fandom/<name>')
def fandom(name):
    """
    Print stories in a fandom.
    """
    fandom = db.session.query(Fandom) \
                       .filter(Fandom.name == name) \
                       .first_or_404()
    stories_page = db.session.query(Story) \
                             .filter(Story.fandom.contains(fandom)) \
                             .paginate()

    return render_template(
        'browse/collection.jinja2',
        endpoint="browse.fandom",
        collection=fandom,
        stories_page=stories_page
    )

@browse.route('/tag/<name>')
def tag(name):
    """
    Print stories in a tag.
    """
    tag = db.session.query(Tag) \
                    .filter(Tag.name == name) \
                    .first_or_404()

    stories_page = db.session.query(Story) \
                             .filter(Story.tags.contains(tag)) \
                             .paginate()

    return render_template(
        'browse/collection.jinja2',
        endpoint="browse.tag",
        collection=tag,
        stories_page=stories_page
    )
