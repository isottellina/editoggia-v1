# post_views.py ---
#
# Filename: post_views.py
# Author: Louise <louise>
# Created: Mon Jun  8 15:08:41 2020 (+0200)
# Last-Updated: Wed Jul  8 02:45:35 2020 (+0200)
#           By: Louise <louise>
#
"""
Views for posting new content (stories and chapters)
"""
from flask import render_template, redirect, url_for, current_app
from flask_login import current_user, login_required

from editoggia.models import Story, Chapter

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
        Chapter.create(
            nb=1,
            content=content,
            story=story
        )

        return redirect(url_for('home.index'))

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
        content = current_app.bleacher.clean(form.data['content'])
        summary = current_app.bleacher.clean(form.data['summary'])

        Chapter.create(
            story=story,
            title=form.data['title'],
            nb=form.data['nb'],
            summary=summary,
            content=content
        )

        return redirect(url_for('home.index'))

    # If we get to this point we should return the form
    # Set a default chapter number (Last chapter + 1)
    form.nb.process_data(story.chapters[-1].nb + 1)

    return render_template('story/post_chapter.jinja2', story=story, form=form)
