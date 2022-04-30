# fandom.py ---
#
# Filename: fandom.py
# Author: Louise <louise>
# Created: Sat May 30 15:14:50 2020 (+0200)
# Last-Updated: Wed Jul 22 01:50:29 2020 (+0200)
#           By: Louise <louise>
#
from editoggia.database import db
from editoggia.models.mixins import CRUDMixin, ModeratedMixin, NameMixin


class FandomCategory(db.Model, CRUDMixin, NameMixin):
    """
    Represent a category of fandom, like “Books” and such.
    """

    __tablename__ = "fandomcategory"

    name = db.Column(db.String(100), nullable=False)
    fandoms = db.relationship("Fandom", back_populates="category")

    def __repr__(self):
        return "<FandomCategory '{}'>".format(self.name)


class Fandom(db.Model, ModeratedMixin):
    """
    Represent a fandom.
    """

    __tablename__ = "fandom"

    category_id = db.Column(db.Integer(), db.ForeignKey("fandomcategory.id"))
    category = db.relationship("FandomCategory", back_populates="fandoms")

    stories = db.relationship(
        "Story", secondary="fandom_stories", back_populates="fandom"
    )

    def __repr__(self):
        return "<Fandom '{}'>".format(self.name)


class FandomStories(db.Model):
    """
    An association table, allowing each story to have several fandoms.
    """

    __tablename__ = "fandom_stories"

    id = db.Column(db.Integer(), primary_key=True)
    fandom_id = db.Column(db.Integer(), db.ForeignKey("fandom.id"))
    story_id = db.Column(db.Integer(), db.ForeignKey("story.id"))
