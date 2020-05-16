# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Thu May 14 18:26:12 2020 (+0200)
# Last-Updated: Sun May 17 00:25:07 2020 (+0200)
#           By: Louise <louise>
#
from flask import render_template, redirect, url_for

from editoggia.database import db
from editoggia.story import story
from editoggia.story.models import Fiction, Chapter

@story.route('/')
def index():
    """
    Show the index of all fictions
    """
    fictions = db.session.query(Fiction).order_by(Fiction.updated_on).all()
    
    return render_template("story/index.jinja2", fictions=fictions)

@story.route('/<int:fiction_id>')
def show_fiction(fiction_id):
    """
    Show a fiction. In practice, redirect to the first chapter if there
    is multiple, and else render the only chapter.
    """
    fiction = Fiction.get_by_id(fiction_id)
    
    if len(fiction.chapters) > 1:
        return redirect(url_for('story.show_chapter',
                                fiction_id=fiction_id,
                                chapter_id=fiction.chapters[0].id)
        )
    else:
        return render_template('story/show_fiction.jinja2',
                               fiction=fiction,
                               chapter=fiction.chapters[0])

@story.route('/<int:fiction_id>/chapter/<chapter_id>')
def show_chapter(fiction_id, chapter_id):
    """
    Show a chapter.
    """
    fiction = Fiction.get_by_id(fiction_id)
    chapter = Chapter.get_by_id(chapter_id)

    return render_template('story/show_chapter.jinja2',
                           fiction=fiction,
                           chapter=chapter)
