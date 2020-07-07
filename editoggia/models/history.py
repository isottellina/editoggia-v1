# history.py --- 
# 
# Filename: history.py
# Author: Louise <louise>
# Created: Tue Jun  9 16:12:19 2020 (+0200)
# Last-Updated: Tue Jul  7 13:49:33 2020 (+0200)
#           By: Louise <louise>
#
from datetime import datetime

from editoggia.database import db
from editoggia.models.mixins import CRUDMixin

class HistoryView(db.Model, CRUDMixin):
    """
    Association table between User and Story.
    It associates a date with it to record when
    the story was visited by the user.
    """
    __tablename__ = 'history_view'
    __table_args__ = (
        # A story can only be added to the history of a user once
        db.UniqueConstraint('user_id', 'story_id', name="unique_history"),
    )

    chapter_nb = db.Column(db.Integer(), nullable=False, default=1)
    date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), nullable=False)
    story_id = db.Column('story_id', db.Integer(), db.ForeignKey('story.id'), nullable=False)
    story = db.relationship('Story')
