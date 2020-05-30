# fandom.py --- 
# 
# Filename: fandom.py
# Author: Louise <louise>
# Created: Sat May 30 15:14:50 2020 (+0200)
# Last-Updated: Sat May 30 15:16:34 2020 (+0200)
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

class Fandom(db.Model, CRUDMixin):
    """
    Represent a fandom. 
    """
    __tablename__ = "fandom"
    
    category_id = db.Column(db.Integer(), db.ForeignKey('fandomcategory.id'),
                            nullable=False)
    category = db.relationship('FandomCategory', back_populates='fandoms')
    
    name = db.Column(db.String(255), index=True, unique=True, nullable=False)
    stories = db.relationship('Story',
                               secondary='story_fandoms',
                               back_populates='fandom')

class StoryFandoms(db.Model):
    """
    An association table, allowing each story to have several fandoms.
    """
    __tablename__ = "story_fandoms"

    id = db.Column(db.Integer(), primary_key=True)
    fandom_id = db.Column(db.Integer(), db.ForeignKey('fandom.id'))
    story_id = db.Column(db.Integer(), db.ForeignKey('story.id'))

from editoggia.models.story import Story
