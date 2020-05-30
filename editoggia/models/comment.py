# comments.py --- 
# 
# Filename: comments.py
# Author: Louise <louise>
# Created: Sat May 30 15:16:18 2020 (+0200)
# Last-Updated: Sat May 30 18:40:57 2020 (+0200)
#           By: Louise <louise>
#
from datetime import datetime

from editoggia.database import db
from editoggia.models.mixins import CRUDMixin

class Comment(db.Model, CRUDMixin):
    content = db.Column(db.Text, nullable=False)

    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
    
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='comments')

    chapter_id = db.Column(db.Integer(), db.ForeignKey('chapter.id'))
    chapter = db.relationship('Chapter', back_populates='comments')

from editoggia.models.user import User
from editoggia.models.story import Chapter
