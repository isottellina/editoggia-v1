# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Thu Jun  4 16:55:50 2020 (+0200)
# Last-Updated: Sat Jun 20 14:36:17 2020 (+0200)
#           By: Louise <louise>
# 
from flask import render_template
from flask.views import View

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

class CollectionView(View):
    """
    Print a collection of stories, be it a fandom or a tag.
    """
    def dispatch_request(self, name):
        collection = db.session.query(self.MODEL) \
                               .filter(self.MODEL.name == name) \
                               .first_or_404()
        stories_page = db.session.query(Story) \
                                 .filter(getattr(Story, self.STORY_FIELD).contains(collection)) \
                                 .paginate()

        return render_template(
            'browse/collection.jinja2',
            endpoint='browse.{}'.format(self.ENDPOINT),
            collection=collection,
            stories_page=stories_page
        )

class FandomView(CollectionView):
    """
    Print all stories in a fandom.
    """
    MODEL = Fandom
    STORY_FIELD = 'fandom'
    ENDPOINT = 'fandom'

class TagView(CollectionView):
    """
    Print all stories in a tag.
    """
    MODEL = Tag
    STORY_FIELD = 'tags'
    ENDPOINT = 'tag'

browse.add_url_rule('/fandom/<name>', view_func=FandomView.as_view(FandomView.ENDPOINT))
browse.add_url_rule('/tag/<name>', view_func=TagView.as_view(TagView.ENDPOINT))
