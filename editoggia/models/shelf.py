# shelf.py ---
#
# Filename: shelf.py
# Author: Louise <louise>
# Created: Fri Jul 17 03:45:44 2020 (+0200)
# Last-Updated: Fri Jul 17 03:58:25 2020 (+0200)
#           By: Louise <louise>
#
from editoggia.database import db
from editoggia.models.mixins import CRUDMixin


class Shelf(db.Model, CRUDMixin):
    __tablename__ = "shelf"
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    color = db.Column(db.String(20), nullable=False, default="")

    stories = db.relationship(
        "Story", secondary="shelves_stories", back_populates="shelves"
    )

    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="shelves")


class ShelvesStories(db.Model):
    __tablename__ = "shelves_stories"

    id = db.Column(db.Integer(), primary_key=True)
    shelf_id = db.Column(
        "shelf_id", db.Integer(), db.ForeignKey("shelf.id"), nullable=False
    )
    story_id = db.Column(
        "story_id", db.Integer(), db.ForeignKey("story.id"), nullable=False
    )
