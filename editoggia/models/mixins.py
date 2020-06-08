# mixins.py --- 
# 
# Filename: mixins.py
# Author: Louise <louise>
# Created: Tue May 19 18:31:47 2020 (+0200)
# Last-Updated: Mon Jun  8 20:08:53 2020 (+0200)
#           By: Louise <louise>
#
from datetime import datetime

from flask import abort
from editoggia.database import db

class PKMixin(object):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    
class CRUDMixin(PKMixin):
    @classmethod
    def get_by_id(cls, id):
        if any((isinstance(id, str) and id.isdigit(),
                isinstance(id, (int, float))),):
            return cls.query.get(int(id))
        return None

    @classmethod
    def get_by_id_or_404(cls, id):
        obj = cls.get_by_id(id)
        if obj is None:
            abort(404)
        return obj

    @classmethod
    def create(cls, commit=True, **kwargs):
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

class ModeratedMixin(object):
    """
    A mixin for moderated objects, such as fandoms or tags.
    It allows for objects to be gotten or created, and set
    to be waiting for moderation. 
    """
    waiting_mod = db.Column(db.Boolean(), nullable=False, default=True)
    
    @classmethod
    def get_or_create(cls, name, **kwargs):
        """
        If the object exists, return it. If
        it doesn't exist, create it, set it
        to be moderated, and return the created one.

        Indexing is done by `name`, and this column must exist.
        If it does not, it will abort with a 500 error.
        """
        if getattr(cls, 'name') is None:
            abort(500)
        obj = cls.query.filter(cls.name == name).first()
        
        if obj:
            return obj
        else:
            return cls.create(
                name=name,
                waiting_mod=True,
                **kwargs
            )

class DatesMixin(object):
    """
    Mixins to add a created_on and updated_on fields
    to a model, automatically set.
    """
    created_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)
