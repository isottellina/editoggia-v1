# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Thu Jun  4 16:55:50 2020 (+0200)
# Last-Updated: Thu Jun  4 17:12:44 2020 (+0200)
#           By: Louise <louise>
# 
from flask import render_template

from editoggia.browse import browse
from editoggia.database import db
from editoggia.models import FandomCategory

@browse.route('/fandoms/<category>')
def fandoms(category):
    """
    Print all fandoms in a category.
    """
    fandomcategory = db.session.query(FandomCategory) \
                               .filter(FandomCategory.name == category) \
                               .first_or_404()

    return render_template('browse/fandoms.jinja2', category=fandomcategory)
