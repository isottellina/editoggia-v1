# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Thu Jun  4 16:55:50 2020 (+0200)
# Last-Updated: Fri Jun 26 16:19:22 2020 (+0200)
#           By: Louise <louise>
# 
from flask import render_template, request, flash, abort
from flask.views import View

from sqlalchemy import func

from editoggia.browse import browse
from editoggia.database import db
from editoggia.models import FandomCategory, Fandom, Story, Tag, User
from editoggia.models import UserLikes, StoryStats

from editoggia.browse.forms import SearchForm

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
    They are all more or less the same, and should all support
    search, so the code is centralized here.
    """
    def dispatch_request(self, name):
        decoded_name = self.MODEL.decode_name(name)
        
        form = SearchForm(request.args)
        if not form.validate():
            print(form.errors)
            abort(400)
        
        collection = db.session.query(self.MODEL) \
                               .filter(self.MODEL.name == decoded_name) \
                               .first_or_404()
        
        b_query = db.session.query(Story) \
                            .filter(getattr(Story, self.STORY_FIELD).contains(collection))

        # Apply different ordering methods
        if form.data['order_by'] == 'title':
            b_query = b_query.order_by(Story.title)
        elif form.data['order_by'] == 'author':
            b_query = b_query.join(User).order_by(User.username)
        elif form.data['order_by'] == 'date_updated':
            b_query = b_query.order_by(Story.updated_on.desc())
        elif form.data['order_by'] == 'hits':
            b_query = b_query.join(StoryStats).order_by(StoryStats.hits.desc())
        elif form.data['order_by'] == 'likes':
            subquery = db.session.query(UserLikes.story_id,
                                        func.count('*').label("likes_count")) \
                                 .group_by(UserLikes.story_id) \
                                 .subquery()
            b_query = b_query.outerjoin(subquery, Story.id==subquery.c.story_id) \
                             .order_by(subquery.c.likes_count.desc())

        return render_template(
            'browse/collection.jinja2',
            endpoint='browse.{}'.format(self.ENDPOINT),
            form=form,
            collection=collection,
            stories_page=b_query.paginate()
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
