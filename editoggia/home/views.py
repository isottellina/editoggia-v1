# views.py ---
#
# Filename: views.py
# Author: Louise <louise>
# Created: Mon May  4 00:22:56 2020 (+0200)
# Last-Updated: Sat May 30 15:17:32 2020 (+0200)
#           By: Louise <louise>
#
from flask import render_template

from editoggia.home import home
from editoggia.database import db
from editoggia.models import FandomCategory, Story


@home.route("/")
def index():
    categories = db.session.query(FandomCategory).all()
    stories = db.session.query(Story).order_by(Story.updated_on.desc())[:3]

    return render_template("home/index.jinja2", categories=categories, stories=stories)
