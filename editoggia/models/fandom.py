# fandom.py --- 
# 
# Filename: fandom.py
# Author: Louise <louise>
# Created: Sat May 30 15:14:50 2020 (+0200)
# Last-Updated: Sun Jun  7 12:48:51 2020 (+0200)
#           By: Louise <louise>
# 
from editoggia.database import db
from editoggia.models.mixins import CRUDMixin

class FandomCategory(db.Model, CRUDMixin):
    """
    Represent a category of fandom, like “Books” and such.
    """
    __tablename__ = "fandomcategory"
    
    name = db.Column(db.String(100), nullable=False)
    fandoms = db.relationship('Fandom', back_populates='category')

    def __repr__(self):
        return "<FandomCategory '{}'>".format(self.name)

class Fandom(db.Model, CRUDMixin):
    """
    Represent a fandom. 
    """
    __tablename__ = "fandom"
    
    category_id = db.Column(db.Integer(), db.ForeignKey('fandomcategory.id'))
    category = db.relationship('FandomCategory', back_populates='fandoms')
    
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    stories = db.relationship('Story',
                               secondary='story_fandoms',
                               back_populates='fandom')
    tags = db.relationship('Tag', secondary='tags_fandoms',
                           back_populates='fandoms')

    # Is this fandom waiting for moderation?
    waiting_mod = db.Column(db.Boolean(), nullable=False, default=True)

    def __repr__(self):
        return "<Fandom '{}'>".format(self.name)

class StoryFandoms(db.Model):
    """
    An association table, allowing each story to have several fandoms.
    """
    __tablename__ = "story_fandoms"

    id = db.Column(db.Integer(), primary_key=True)
    fandom_id = db.Column(db.Integer(), db.ForeignKey('fandom.id'))
    story_id = db.Column(db.Integer(), db.ForeignKey('story.id'))

from editoggia.models.story import Story
from editoggia.models.tag import Tag
