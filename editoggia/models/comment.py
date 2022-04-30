# comments.py ---
#
# Filename: comments.py
# Author: Louise <louise>
# Created: Sat May 30 15:16:18 2020 (+0200)
# Last-Updated: Mon Jun  8 20:08:57 2020 (+0200)
#           By: Louise <louise>
#
from editoggia.database import db
from editoggia.models.mixins import CRUDMixin, DatesMixin


class Comment(db.Model, CRUDMixin, DatesMixin):
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    author = db.relationship("User", back_populates="comments")

    chapter_id = db.Column(db.Integer(), db.ForeignKey("chapter.id"))
    chapter = db.relationship("Chapter", back_populates="comments")
