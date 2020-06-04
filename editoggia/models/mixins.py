# mixins.py --- 
# 
# Filename: mixins.py
# Author: Louise <louise>
# Created: Tue May 19 18:31:47 2020 (+0200)
# Last-Updated: Thu Jun  4 21:08:19 2020 (+0200)
#           By: Louise <louise>
#
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
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

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
