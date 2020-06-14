# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Thu May 14 18:26:12 2020 (+0200)
# Last-Updated: Sun Jun 14 14:09:03 2020 (+0200)
#           By: Louise <louise>
#
from flask import render_template, redirect, url_for
from flask_login import current_user

from editoggia.database import db
from editoggia.story import story

from editoggia.models import Story, Chapter

@story.route('/')
def index():
    """
    Show the index of all stories
    """
    stories = db.session.query(Story).order_by(Story.updated_on.desc()).all()
    
    return render_template("story/index.jinja2", stories=stories)
    
@story.route('/<int:story_id>')
def show_story(story_id):
    """
    Show a story. In practice, redirect to the first chapter if there
    is multiple, and else render the only chapter.
    """
    story = Story.get_by_id_or_404(story_id)
    
    if len(story.chapters) > 1:
        return redirect(url_for('story.show_chapter',
                                story_id=story_id,
                                chapter_id=story.chapters[0].id)
        )
    else:
        current_user.add_to_history(story)
        story.hit()
        return render_template('story/show_chapter.jinja2',
                               story=story,
                               chapter=story.chapters[0])

@story.route('/<int:story_id>/chapter/<chapter_id>')
def show_chapter(story_id, chapter_id):
    """
    Show a chapter.
    """
    story = Story.get_by_id_or_404(story_id)
    chapter = Chapter.get_by_id_or_404(chapter_id)

    current_user.add_to_history(story)
    story.hit()
    
    return render_template('story/show_chapter.jinja2',
                           story=story,
                           chapter=chapter)

@story.route('/<int:story_id>/index')
def story_index(story_id):
    """
    Show the index of a particular story.
    """
    story = Story.get_by_id_or_404(story_id)

    return render_template('story/story_index.jinja2', story=story)
