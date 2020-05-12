# models.py --- 
# 
# Filename: models.py
# Author: Louise <louise>
# Created: Tue May 12 20:59:45 2020 (+0200)
# Last-Updated: Tue May 12 21:06:59 2020 (+0200)
#           By: Louise <louise>
# 
from app.database import db

class Language(db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
