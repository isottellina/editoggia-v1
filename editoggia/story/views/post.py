# post_views.py ---
#
# Filename: post_views.py
# Author: Louise <louise>
# Created: Mon Jun  8 15:08:41 2020 (+0200)
# Last-Updated: Tue Jul  7 21:11:58 2020 (+0200)
#           By: Louise <louise>
#
import bleach

from flask import render_template, redirect, url_for, current_app
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

    if form.validate_on_submit():
        # First we have to bleach the HTML content we got
        summary = current_app.bleacher.clean(form.data['summary'])
        content = current_app.bleacher.clean(form.data['content'])

        # We have to create the story before the chapter
        story = Story.create(
            title=form.data['title'],
            rating=form.data['rating'],
            author=current_user,
            summary=summary,
            fandom=form.data['fandom'],
            tags=form.data['tags'],
            total_chapters=form.data['total_chapters']
        )

        # Then we create the first chapter
        chapter = Chapter.create(
            nb=1,
            content=content,
            story=story
        )

        return redirect(url_for('home.index'))
    else:
        form.populate_select2()
        return render_template('story/post_story.jinja2', form=form)

@story.route('/post/<int:story_id>/chapter', methods=["GET", "POST"])
@login_required
def post_chapter(story_id):
    """
    Post a new chapter.
    """
    story = Story.get_by_id_or_404(story_id)
    form = ChapterForm(story=story)

    if form.validate_on_submit():
        # First we have to bleach the HTML content we got
        content = bleach.clean(form.data['content'])
        summary = bleach.clean(form.data['summary'])

        Chapter.create(
            story=story,
            title=form.data['title'],
            nb=form.data['nb'],
            summary=summary,
            content=content
        )

        return redirect(url_for('home.index'))
    else:
        # Set a default chapter number (Last chapter + 1)
        form.nb.process_data(story.chapters[-1].nb + 1)

        return render_template('story/post_chapter.jinja2', story=story, form=form)
