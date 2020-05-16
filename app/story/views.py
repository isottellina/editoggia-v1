# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Thu May 14 18:26:12 2020 (+0200)
# Last-Updated: Sat May 16 17:40:07 2020 (+0200)
#           By: Louise <louise>
#
from flask import render_template, redirect, url_for

from app.database import db
from app.story import story
from app.story.models import Fiction, Chapter

@story.route('/')
def index():
    fictions = db.session.query(Fiction).order_by(Fiction.updated_on).all()
    
    return render_template("story/index.jinja2", fictions=fictions)

@story.route('/<int:fiction_id>')
def show_fiction(fiction_id):
    chapter = db.session.query(Chapter).filter(Chapter.fiction_id == fiction_id) \
                                       .filter(Chapter.nb == 0) \
                                       .first()
    
    return redirect(url_for('story.show_chapter',
                            fiction_id=fiction_id,
                            chapter_id=chapter.id)
    )

@story.route('/<int:fiction_id>/chapter/<chapter_id>')
def show_chapter(fiction_id, chapter_id):
    chapter = db.session.query(Chapter).filter(Chapter.id == chapter_id) \
                                       .first()

    return render_template('story/show_chapter.jinja2', chapter=chapter)
