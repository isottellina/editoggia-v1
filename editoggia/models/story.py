# models.py --- 
# 
# Filename: models.py
# Author: Louise <louise>
# Created: Thu May 14 18:25:31 2020 (+0200)
# Last-Updated: Mon Jun  8 14:58:06 2020 (+0200)
#           By: Louise <louise>
#
"""
The models for the story blueprint.
"""
from datetime import datetime

from flask_babel import gettext
from editoggia.database import db
from editoggia.models.mixins import PKMixin, CRUDMixin

class Story(db.Model, CRUDMixin):
    """
    A story, written on the site.
    """
    __tablename__ = "story"

    title = db.Column(db.String(255), nullable=False, index=True)
    summary = db.Column(db.String(1000), nullable=False, default="")
    hits = db.Column(db.Integer(), nullable=False, default=0, index=True)
    total_chapters = db.Column(db.Integer())

    rating = db.Column(db.Enum(
        gettext("General audiences"),
        gettext("Teen and up audiences"),
        gettext("Mature"),
        gettext("Explicit")
    ))

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
                               cascade='all, delete, delete-orphan',
                               order_by='Chapter.nb')
    tags = db.relationship('Tag', secondary='stories_tags',
                           back_populates='stories')

    user_likes = db.relationship(
        'User', secondary='user_likes',
        back_populates='likes'
    )

    def __setattr__(self, attr, value):
        """
        We overload this method to allow for special behaviour
        for the fandom and tag fields. Hereby, we can set their
        fields with strings and actually set the objects.
        """
        # We import the models here to ensure that there be no
        # issues loading the file.
        from editoggia.models import Fandom

        # The second check checks that the first element in the
        # list exists, and that it's a string. If there is no
        # first element, or if the value is already a model,
        # we have no need for the transformation.
        if attr == "fandom" and type(next(iter(value), 0)) == str:
            value = [Fandom.get_or_create(fandom) for fandom in value]
        
        db.Model.__setattr__(self, attr, value)
    
    def __repr__(self):
        return "<Story '{}', by '{}'>".format(self.title, self.author)

    def hit(self):
        """
        If user is not the author, increment hit.
        """
        from flask_login import current_user
        
        if current_user != self.author:
            self.hits += 1
            db.session.commit()

class StoryStats(db.Model, PKMixin):
    hits = db.Column(db.Integer(), nullable=False, default=0, index=True)
    
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

    comments = db.relationship('Comment', back_populates='chapter')

    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    story_id = db.Column(db.Integer(), db.ForeignKey('story.id'),
                         nullable=False)
    story = db.relationship('Story', back_populates='chapters')
    
    def __repr__(self):
        return "<Chapter {} of story '{}', by '{}'>".format(
            self.nb,
            self.story.title,
            self.story.author
        )

from editoggia.models.user import User
from editoggia.models.fandom import Fandom
from editoggia.models.comment import Comment
from editoggia.models.tag import Tag
