# tag.py --- 
# 
# Filename: tag.py
# Author: Louise <louise>
# Created: Sun Jun  7 12:32:42 2020 (+0200)
# Last-Updated: Sun Jun  7 21:21:30 2020 (+0200)
#           By: Louise <louise>
#
from flask_babel import gettext
from editoggia.database import db
from editoggia.models.mixins import CRUDMixin, ModeratedMixin

class Tag(db.Model, CRUDMixin, ModeratedMixin):
    """
    A tag. I really don't know how else to describe it.
    """
    __tablename__ = "tag"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    # The tag type. It can only be null in the case of a tag awaiting
    # moderation.
    tag_type = db.Column(db.Enum(
        "General",
        "Characters",
        "Relationship",
    ))
    
    fandoms = db.relationship('Fandom', secondary='tags_fandoms',
                              back_populates='tags')
    stories = db.relationship('Story', secondary='stories_tags',
                              back_populates='tags')

class TagsFandoms(db.Model):
    """
    Association table between Tags and Fandom. It is used to note
    that certain tags only apply to certain fandoms.
    """
    __tablename__ = "tags_fandoms"

    id = db.Column(db.Integer(), primary_key=True)
    tag_id = db.Column(db.Integer(), db.ForeignKey('tag.id'))
    fandom_id = db.Column(db.Integer(), db.ForeignKey('fandom.id'))
    
class StoriesTags(db.Model):
    """
    Association table between Story and Tags.
    """
    __tablename__ = "stories_tags"

    id = db.Column(db.Integer(), primary_key=True)
    story_id = db.Column(db.Integer(), db.ForeignKey('story.id'))
    tag_id = db.Column(db.Integer(), db.ForeignKey('tag.id'))
    
from editoggia.models.story import Story
from editoggia.models.fandom import Fandom
