# edit_views.py --- 
# 
# Filename: edit_views.py
# Author: Louise <louise>
# Created: Mon Jun  8 15:10:40 2020 (+0200)
# Last-Updated: Thu Jun 11 15:55:06 2020 (+0200)
#           By: Louise <louise>
#
import bleach

from flask import render_template, redirect, abort, url_for
from flask_login import current_user, login_required

from editoggia.database import db
from editoggia.models import Fandom, Story, Chapter, Tag

from editoggia.story import story
from editoggia.story.forms import EditStoryForm, ChapterForm

def populate_select_field(model, base, field):
    field.choices = [
        (base_sgl.name, base_sgl.name)
        for base_sgl in base
    ]
    field.process_data([base_sgl.name for base_sgl in base])

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
    
    if form.validate_on_submit():
        # We update the story
        form.populate_obj(story)
        story.update()
        
        return redirect(url_for('home.index'))
    else:
        populate_select_field(Fandom, story.fandom, form.fandom)
        populate_select_field(Tag, story.tags, form.tags)
        
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
