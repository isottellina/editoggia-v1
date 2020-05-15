# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Thu May 14 18:26:12 2020 (+0200)
# Last-Updated: Fri May 15 21:30:34 2020 (+0200)
#           By: Louise <louise>
#
from flask import render_template

from app.database import db
from app.story import story
from app.story.models import Fiction

@story.route('/')
def index():
    fictions = db.session.query(Fiction).order_by(Fiction.updated_on).all()
    
    return render_template("story/index.jinja2", fictions=fictions)
