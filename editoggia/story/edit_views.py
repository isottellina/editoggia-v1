# edit_views.py --- 
# 
# Filename: edit_views.py
# Author: Louise <louise>
# Created: Mon Jun  8 15:10:40 2020 (+0200)
# Last-Updated: Mon Jun  8 15:16:48 2020 (+0200)
#           By: Louise <louise>
#
import bleach

from flask import render_template, redirect, abort, url_for
from flask_login import current_user, login_required

from editoggia.database import db
from editoggia.models import Fandom, Story, Chapter

from editoggia.story import story
from editoggia.story.forms import EditStoryForm, ChapterForm

@story.route('/edit/<int:story_id>', methods=["GET", "POST"])
@login_required
def edit_story(story_id):
    """
    Edit a story.
    """
    # The story has to exist and to have been written by the
    # current user
    story = Story.get_by_id_or_404(story_id)
    if story.author != current_user:
        abort(403)
        
    form = EditStoryForm(obj=story)

    # We have to populate the fandom field
    fandoms = db.session.query(Fandom).all()
    form.fandom.choices = [
        (fandom.name, fandom.name) for fandom in fandoms
    ]
    form.characters.choices = []
    form.relationships.choices = []
    form.tags.choices = []
    
    if form.validate_on_submit():
        # We update the story
        form.populate_obj(story)
        story.update()
        
        return redirect(url_for('home.index'))
    else:
        # Select the right fandoms
        form.fandom.process_data([fandom.name for fandom in story.fandom])
        
        return render_template('story/edit_story.jinja2', form=form, story=story)

@story.route('/edit/<int:story_id>/chapter/<int:chapter_id>', methods=["GET", "POST"])
@login_required
def edit_chapter(story_id, chapter_id):
    """
    Edit a chapter
    """
    # The story has to exist and to have been written by the
    # current user
    chapter = Chapter.get_by_id_or_404(chapter_id)
    if chapter.story.author != current_user:
        abort(403)
        
    form = ChapterForm(obj=chapter)
    
    if form.validate_on_submit():
        form.data['content'] = bleach.clean(form.data['content'])
        
        form.populate_obj(chapter)
        chapter.update()
        
        return redirect(url_for('home.index'))
    else:
        return render_template('story/edit_chapter.jinja2', form=form, chapter=chapter)
