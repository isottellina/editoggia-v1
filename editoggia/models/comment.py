# comments.py --- 
# 
# Filename: comments.py
# Author: Louise <louise>
# Created: Sat May 30 15:16:18 2020 (+0200)
# Last-Updated: Sat May 30 15:28:28 2020 (+0200)
#           By: Louise <louise>
# 
from editoggia.database import db
from editoggia.models.mixins import CRUDMixin

class Comment(db.Model, CRUDMixin):
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='comments')

    chapter_id = db.Column(db.Integer(), db.ForeignKey('chapter.id'))
    chapter = db.relationship('Chapter', back_populates='comments')

from editoggia.models.user import User
from editoggia.models.story import Chapter
