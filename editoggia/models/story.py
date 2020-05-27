# models.py --- 
# 
# Filename: models.py
# Author: Louise <louise>
# Created: Thu May 14 18:25:31 2020 (+0200)
# Last-Updated: Wed May 27 18:57:33 2020 (+0200)
#           By: Louise <louise>
#
"""
The models for the story blueprint.
"""
from datetime import datetime

from flask_babel import gettext
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
    
    
class Story(db.Model, CRUDMixin):
    """
    A story, written on the site.
    """
    __tablename__ = "story"

    title = db.Column(db.String(255), nullable=False, index=True)
    summary = db.Column(db.String(1000), nullable=False, default="")
    hits = db.Column(db.Integer(), nullable=False, default=0, index=True)
    total_chapters = db.Column(db.Integer())

    fandom = db.relationship('Fandom',
                             secondary='story_fandoms',
                             back_populates='stories')

    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'),
                          nullable=False)
    author = db.relationship('User', back_populates='stories')

    chapters = db.relationship('Chapter', back_populates='story',
                               order_by='Chapter.nb')
    tags = db.relationship('Tag', secondary='stories_tags',
                           back_populates='stories')

    user_likes = db.relationship(
        'User',
        secondary='user_likes', lazy='dynamic',
        back_populates='likes'
    )

    def hit(self):
        """
        If user is not the author, increment hit.
        """
        from flask_login import current_user
        
        if current_user != self.author:
            self.hits += 1
            db.session.commit()

    
def chapter_get_new_nb(context):
    """
    Returns the new number for a chapter for a given story.
    """
    def is_persistent(obj):
        """
        Returns if an object is persistent, so we can
        filter out transient or pending objects.
        """
        return db.inspect(obj).persistent
    
    story_id = context.get_current_parameters()['story_id']
    story = Story.get_by_id(story_id)

    persistent_chapters = list(filter(is_persistent, story.chapters))
    
    if len(persistent_chapters) == 0:
        return 1
    else:
        return persistent_chapters[-1].nb + 1
    
class Chapter(db.Model, CRUDMixin):
    """
    A chapter. Simple as that.
    """
    __tablename__ = "chapter"

    nb = db.Column(db.Integer(),
                   default=chapter_get_new_nb,
                   nullable=False, index=True)

    title = db.Column(db.String(255), nullable=False, default="")
    summary = db.Column(db.Text())
    content = db.Column(db.Text(), nullable=False)

    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    story_id = db.Column(db.Integer(), db.ForeignKey('story.id'))
    story = db.relationship('Story', back_populates='chapters')


class StoriesTags(db.Model):
    """
    Association table between Story and Tags.
    """
    __tablename__ = "stories_tags"

    id = db.Column(db.Integer(), primary_key=True)
    story_id = db.Column(db.Integer(), db.ForeignKey('story.id'))
    tag_id = db.Column(db.Integer(), db.ForeignKey('tag.id'))

class Tag(db.Model, CRUDMixin):
    """
    A tag. I really don't know how else to describe it.
    """
    __tablename__ = "tag"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    stories = db.relationship('Story', secondary='stories_tags',
                               back_populates='tags')

from editoggia.models.user import User
