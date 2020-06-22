# models.py --- 
# 
# Filename: models.py
# Author: Louise <louise>
# Created: Thu May 14 18:25:31 2020 (+0200)
# Last-Updated: Mon Jun 22 21:50:23 2020 (+0200)
#           By: Louise <louise>
#
"""
The models for the story blueprint.
"""
from flask_babel import gettext
from editoggia.database import db
from editoggia.models.mixins import PKMixin, CRUDMixin, DatesMixin

class Story(db.Model, CRUDMixin, DatesMixin):
    """
    A story, written on the site.
    """
    __tablename__ = "story"

    title = db.Column(db.String(255), nullable=False, index=True)
    summary = db.Column(db.String(1000), nullable=False, default="")
    total_chapters = db.Column(db.Integer())

    rating = db.Column(db.Enum(
        gettext("General audiences"),
        gettext("Teen and up audiences"),
        gettext("Mature"),
        gettext("Explicit")
    ))

    fandom = db.relationship('Fandom',
                             secondary='fandom_stories',
                             back_populates='stories')

    stats_id = db.Column(db.Integer(), db.ForeignKey('storystats.id'),
                         nullable=False)
    stats = db.relationship('StoryStats', back_populates='story')
    
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'),
                          nullable=False)
    author = db.relationship('User', back_populates='stories')

    chapters = db.relationship('Chapter', back_populates='story',
                               cascade='all, delete, delete-orphan',
                               order_by='Chapter.nb')
    tags = db.relationship('Tag', secondary='story_tags',
                           back_populates='stories')

    user_likes = db.relationship(
        'User', secondary='user_likes',
        back_populates='likes'
    )

    @classmethod
    def create(cls, commit=True, **kwargs):
        """
        We overload the create method to create automatically
        the Story and the StoryStats object.
        """
        stats = StoryStats()
        story = Story(
            stats=stats,
            **kwargs
        )

        return story.save()
    
    def hit(self):
        """
        If user is not the author, increment hit.
        Should only be called once per registrated
        user.
        """
        from flask_login import current_user
        
        if current_user != self.author:
            self.stats.hits += 1
            db.session.commit()

    def __setattr__(self, attr, value):
        """
        We overload this method to allow for special behaviour
        for the fandom and tag fields. Hereby, we can set their
        fields with strings and actually set the objects.
        """
        # We import the models here to ensure that there be no
        # issues loading the file.
        from editoggia.models import Fandom, Tag

        # The second check checks that the first element in the
        # list exists, and that it's a string. If there is no
        # first element, or if the value is already a model,
        # we have no need for the transformation.
        if attr == "fandom" and type(next(iter(value), 0)) == str:
            value = [Fandom.get_or_create(fandom) for fandom in value]
        if attr == "tags" and type(next(iter(value), 0)) == str:
            value = [Tag.get_or_create(tag) for tag in value]
            
        db.Model.__setattr__(self, attr, value)
    
    def __repr__(self):
        return "<Story '{}', by '{}'>".format(self.title, self.author)

class StoryStats(db.Model, PKMixin):
    __tablename__ = "storystats"
    
    hits = db.Column(db.Integer(), nullable=False, default=0)
    story = db.relationship('Story', back_populates='stats')
    
class Chapter(db.Model, CRUDMixin, DatesMixin):
    """
    A chapter. Simple as that.
    """
    __tablename__ = "chapter"
    __table_args__ = (
        # There can only be one chapter with a certain number by
        # story ID.
        db.UniqueConstraint('nb', 'story_id', name="unique_chapter_nb"),
    )

    nb = db.Column(db.Integer(), nullable=False, index=True)

    title = db.Column(db.String(255), nullable=False, default="")
    summary = db.Column(db.Text())
    content = db.Column(db.Text(), nullable=False)

    comments = db.relationship('Comment', back_populates='chapter')

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
