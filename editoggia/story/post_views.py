# post_views.py --- 
# 
# Filename: post_views.py
# Author: Louise <louise>
# Created: Mon Jun  8 15:08:41 2020 (+0200)
# Last-Updated: Mon Jun  8 15:27:22 2020 (+0200)
#           By: Louise <louise>
#
import bleach

from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from editoggia.database import db
from editoggia.models import Fandom, Story, Chapter

from editoggia.story import story
from editoggia.story.forms import PostStoryForm, ChapterForm

@story.route('/post', methods=["GET", "POST"])
@login_required
def post_story():
    """
    Post a new story.
    """
    form = PostStoryForm()

    # We have to populate the fandom field
    fandoms = db.session.query(Fandom).all()
    form.fandom.choices = [
        (fandom.name, fandom.name) for fandom in fandoms
    ]
    
    if form.validate_on_submit():
        # First we have to bleach the HTML content we got
        content = bleach.clean(form.data['content'])
        
        # We have to create the story before the chapter
        story = Story.create(
            title=form.data['title'],
            rating=form.data['rating'],
            author=current_user,
            summary=form.data['summary'],
            fandom=form.data['fandom']
        )

        # Then we create the first chapter
        chapter = Chapter.create(
            content=content,
            story=story
        )
        
        return redirect(url_for('home.index'))
    else:
        return render_template('story/post_story.jinja2', form=form)

@story.route('/post/<int:story_id>/chapter', methods=["GET", "POST"])
@login_required
def post_chapter(story_id):
    """
    Post a new story.
    """
    story = Story.get_by_id_or_404(story_id)
    form = ChapterForm()
    
    if form.validate_on_submit():
        # First we have to bleach the HTML content we got
        content = bleach.clean(form.data['content'])

        Chapter.create(
            story=story,
            title=form.data['title'],
            nb=form.data['nb'],
            summary=form.data['summary'],
            content=content
        )
        
        return redirect(url_for('home.index'))
    else:
        # Set a default chapter number (Last chapter + 1)
        form.nb.process_data(story.chapters[-1].nb + 1)
        
        return render_template('story/post_chapter.jinja2', story=story, form=form)
