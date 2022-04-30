# views.py ---
#
# Filename: views.py
# Author: Louise <louise>
# Created: Thu Jun  4 16:55:50 2020 (+0200)
# Last-Updated: Thu Jul  9 14:25:18 2020 (+0200)
#           By: Louise <louise>
#
from flask import abort, render_template, request
from flask.views import View
from sqlalchemy import func

from editoggia.browse import browse
from editoggia.browse.forms import SearchForm
from editoggia.database import db
from editoggia.models import (
    Fandom,
    FandomCategory,
    Story,
    StoryStats,
    Tag,
    User,
    UserLikes,
)


@browse.route("/fandoms/<category>")
def fandoms(category):
    """
    Print all fandoms in a category.
    """
    fandomcategory = (
        db.session.query(FandomCategory)
        .filter(FandomCategory.name == category)
        .first_or_404()
    )

    return render_template("browse/fandoms.jinja2", category=fandomcategory)


class CollectionView(View):
    """
    Print a collection of stories, be it a fandom or a tag.
    They are all more or less the same, and should all support
    search, so the code is centralized here.
    """

    def dispatch_request(self, name):
        form = SearchForm(request.args)
        if not form.validate():
            abort(400)

        collection = self.MODEL.get_by_encoded_name_or_404(name)
        b_query = db.session.query(Story).filter(
            getattr(Story, self.STORY_FIELD).contains(collection)
        )

        # Options
        if form.data["rating"]:
            b_query = b_query.filter(Story.rating == form.data["rating"])

        # Include fandoms in query
        for fandom_name in form.data["included_fandom"]:
            fandom = Fandom.get_by_name_or_404(fandom_name)
            b_query = b_query.filter(Story.fandom.contains(fandom))

        # Include tags in query
        for tag_name in form.data["included_tags"]:
            tag = Tag.get_by_name_or_404(tag_name)
            b_query = b_query.filter(Story.tags.contains(tag))

        # Exclude tags from query
        for tag_name in form.data["excluded_tags"]:
            tag = Tag.get_by_name_or_404(tag_name)
            b_query = b_query.filter(~Story.tags.contains(tag))

        # Apply different ordering methods
        if form.data["order_by"] == "title":
            b_query = b_query.order_by(Story.title)
        elif form.data["order_by"] == "author":
            b_query = b_query.join(User).order_by(User.username)
        elif form.data["order_by"] == "date_updated":
            b_query = b_query.order_by(Story.updated_on.desc())
        elif form.data["order_by"] == "hits":
            b_query = b_query.join(StoryStats).order_by(StoryStats.hits.desc())
        elif form.data["order_by"] == "likes":
            subquery = (
                db.session.query(
                    UserLikes.story_id, func.count("*").label("likes_count")
                )
                .group_by(UserLikes.story_id)
                .subquery()
            )
            b_query = b_query.outerjoin(
                subquery, Story.id == subquery.c.story_id
            ).order_by(func.coalesce(subquery.c.likes_count, 0).desc())

        return render_template(
            "browse/collection.jinja2",
            endpoint="browse.{}".format(self.ENDPOINT),
            form=form,
            collection=collection,
            stories_page=b_query.paginate(),
        )


class FandomView(CollectionView):
    """
    Print all stories in a fandom.
    """

    MODEL = Fandom
    STORY_FIELD = "fandom"
    ENDPOINT = "fandom"


class TagView(CollectionView):
    """
    Print all stories in a tag.
    """

    MODEL = Tag
    STORY_FIELD = "tags"
    ENDPOINT = "tag"


browse.add_url_rule("/fandom/<name>", view_func=FandomView.as_view(FandomView.ENDPOINT))
browse.add_url_rule("/tag/<name>", view_func=TagView.as_view(TagView.ENDPOINT))
