# tag.py ---
#
# Filename: tag.py
# Author: Louise <louise>
# Created: Sun Jun  7 12:32:42 2020 (+0200)
# Last-Updated: Wed Jul 22 01:50:46 2020 (+0200)
#           By: Louise <louise>
#
from flask_babelex import gettext
from editoggia.database import db
from editoggia.models.mixins import CRUDMixin, ModeratedMixin


class Tag(db.Model, ModeratedMixin):
    """
    A tag. I really don't know how else to describe it.
    """

    __tablename__ = "tag"

    stories = db.relationship("Story", secondary="story_tags", back_populates="tags")


class StoryTags(db.Model):
    """
    Association table between Story and Tags.
    """

    __tablename__ = "story_tags"

    id = db.Column(db.Integer(), primary_key=True)
    story_id = db.Column(db.Integer(), db.ForeignKey("story.id"))
    tag_id = db.Column(db.Integer(), db.ForeignKey("tag.id"))


from editoggia.models.story import Story
from editoggia.models.fandom import Fandom
