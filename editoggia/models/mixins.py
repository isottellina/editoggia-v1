# mixins.py ---
#
# Filename: mixins.py
# Author: Louise <louise>
# Created: Tue May 19 18:31:47 2020 (+0200)
# Last-Updated: Fri Jul 17 17:00:05 2020 (+0200)
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
        """
        Create a new record.
        """
        instance = cls(**kwargs)
        return instance.save(commit=commit)

    def update(self, commit=True, **kwargs):
        """
        Update all given fields of a record.
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def touch(self):
        """
        Touch a record. Triggers all onupdate
        functions but doesn't update other fields.
        """
        stmt = db.update(type(self)).where(type(self).id == self.id)
        db.engine.execute(stmt)

    def save(self, commit=True):
        """
        Saves a record to the session.
        """
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """
        Delete a record.
        """
        db.session.delete(self)
        return commit and db.session.commit()

class NameMixin(object):
    """
    A mixin for models that have a name, and can be encoded to be
    in the URL.
    """
    __table_args__ = {'extend_existing': True}

    name = db.Column(db.String(255), unique=True, nullable=False)

    @classmethod
    def get_by_name(cls, name):
        """
        Returns an object by its name.
        """
        return cls.query.filter(cls.name == name).first()

    @classmethod
    def get_by_name_or_404(cls, name):
        """
        Same as get_by_name, but issues a 404 error if None.
        """
        return cls.query.filter(cls.name == name).first_or_404()

    @classmethod
    def get_by_encoded_name_or_404(cls, encoded_name):
        """
        Same as get_by_name_or_404, but uses the URL-encoded name.
        """
        name = cls.decode_name(encoded_name)
        return cls.get_by_name_or_404(name)

    def encode_name(self):
        """
        Replace URL-sensitive characters.
        """
        return self.name.replace('&', '*a*') \
                        .replace('/', '*s*')

    @staticmethod
    def decode_name(name):
        """
        Does the inverse operation.
        """
        return name.replace('*a*', '&') \
                   .replace('*s*', '/')

class ModeratedMixin(CRUDMixin, NameMixin):
    """
    A mixin for moderated objects, such as fandoms or tags.
    It allows for objects to be gotten or created, and set
    to be waiting for moderation. Implies name mixin.
    """
    waiting_mod = db.Column(db.Boolean(), nullable=False, default=True)

    @classmethod
    def get_or_create(cls, name, **kwargs):
        """
        If the object exists, return it. If
        it doesn't exist, create it, set it
        to be moderated, and return the created one.
        """
        return cls.get_by_name(name) or cls.create(
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
