# views.py --- 
# 
# Filename: views.py
# Author: Louise <louise>
# Created: Thu May 14 18:26:12 2020 (+0200)
# Last-Updated: Sat May 30 15:18:36 2020 (+0200)
#           By: Louise <louise>
#
import bleach

from flask import render_template, redirect, url_for, abort
from flask_login import login_required, current_user

from editoggia.database import db
from editoggia.story import story
from editoggia.story.forms import StoryForm

from editoggia.models import Fandom, Story, Chapter

@story.route('/')
def index():
    """
    Show the index of all stories
    """
    stories = db.session.query(Story).order_by(Story.updated_on.desc()).all()
    
    return render_template("story/index.jinja2", stories=stories)

@story.route('/post', methods=["GET", "POST"])
@login_required
def post_story():
    """
    Post a new story.
    """
    form = StoryForm()

    # We have to populate the fandom field
    fandoms = db.session.query(Fandom).all()
    form.fandom.choices = [
        (fandom.name, fandom.name) for fandom in fandoms
    ]
    
    if form.validate_on_submit():
        # First we have to bleach the HTML content we got
        content = bleach.clean(form.data['content'])
        
        # We have to load the fandoms
        loaded_fandoms = [
            db.session.query(Fandom).filter(Fandom.name==fandom).first_or_404()
            for fandom in form.data['fandom']
        ]
        
        # We have to create the story before the chapter
        story = Story.create(
            title=form.data['title'],
            author=current_user,
            summary=form.data['summary'],
            fandom=loaded_fandoms
        )

        # Then we create the first chapter
        chapter = Chapter.create(
            content=content,
            story=story
        )
        
        return redirect(url_for('home.index'))
    else:
        return render_template('story/post_story.jinja2', form=form)

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
