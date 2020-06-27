# edit_views.py --- 
# 
# Filename: edit_views.py
# Author: Louise <louise>
# Created: Mon Jun  8 15:10:40 2020 (+0200)
# Last-Updated: Sat Jun 27 14:01:28 2020 (+0200)
#           By: Louise <louise>
#
import bleach

from flask import render_template, redirect, abort, url_for
from flask_login import current_user, login_required

from editoggia.database import db
from editoggia.models import Fandom, Story, Chapter, Tag

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
    
    if form.validate_on_submit():
        # Bleach summary
        form.data['summary'] = bleach.clean(form.data['summary'])
        
        # We update the story
        form.populate_obj(story)
        story.update()
        
        return redirect(url_for('home.index'))
    else:
        form.populate_select2(story.fandom, story.tags)
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
        
    form = ChapterForm(obj=chapter, chapter=chapter, story=chapter.story)
    
    if form.validate_on_submit():
        form.data['content'] = bleach.clean(form.data['content'])
        form.data['summary'] = bleach.clean(form.data['summary'])
        
        form.populate_obj(chapter)
        chapter.update()
        
        return redirect(url_for('home.index'))
    else:
        return render_template('story/edit_chapter.jinja2', form=form, chapter=chapter)
