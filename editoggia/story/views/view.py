# views.py ---
#
# Filename: views.py
# Author: Louise <louise>
# Created: Thu May 14 18:26:12 2020 (+0200)
# Last-Updated: Wed Feb 10 14:09:45 2021 (+0100)
#           By: Louise <louise>
#
"""
Views for viewing stories and chapters.
"""
from flask import redirect, render_template, url_for
from flask_login import current_user

from editoggia.database import db
from editoggia.models import Chapter, Story
from editoggia.story import story
from editoggia.story.forms import CommentForm, LikeForm


@story.route("/")
def index():
    """
    Show the last 20 stories.
    """
    stories = db.session.query(Story).order_by(Story.updated_on.desc()).limit(20).all()

    return render_template("story/index.jinja2", stories=stories)


@story.route("/<int:story_id>")
def show_story(story_id):
    """
    Show a story. In practice, redirect to a chapter if there
    is multiple, and else render the only chapter.
    """
    story = Story.get_by_id_or_404(story_id)

    if len(story.chapters) > 1:
        # If story has multiple chapters, restore the progression of the
        # user.
        history = current_user.get_from_history(story)

        if history is None:
            # If we have no history, redirect to the first chapter.
            return redirect(
                url_for(
                    "story.show_chapter",
                    story_id=story_id,
                    chapter_id=story.chapters[0].id,
                )
            )

        return redirect(
            url_for(
                "story.show_chapter",
                story_id=story_id,
                chapter_id=story.chapters[history.chapter_nb - 1].id,
            )
        )

    # If we get to this point, we just load the first chapter since it's a
    # 1-chapter story.
    like_form = LikeForm()
    comment_form = CommentForm()

    current_user.add_to_history(story)
    return render_template(
        "story/show_chapter.jinja2",
        like_form=like_form,
        comment_form=comment_form,
        story=story,
        chapter=story.chapters[0],
    )


@story.route("/<int:story_id>/full")
def show_full_story(story_id):
    """
    Show a full story.
    """
    story = Story.get_by_id_or_404(story_id)

    current_user.add_to_history(story)
    return render_template("story/show_full_story.jinja2", story=story)


@story.route("/<int:story_id>/chapter/<chapter_id>")
def show_chapter(story_id, chapter_id):
    """
    Show a chapter.
    """
    story = Story.get_by_id_or_404(story_id)
    chapter = Chapter.get_by_id_or_404(chapter_id)

    like_form = LikeForm()
    comment_form = CommentForm()

    current_user.add_to_history(story, chapter.nb)
    return render_template(
        "story/show_chapter.jinja2",
        like_form=like_form,
        comment_form=comment_form,
        story=story,
        chapter=chapter,
    )


@story.route("/<int:story_id>/index")
def story_index(story_id):
    """
    Show the index of a particular story.
    """
    story = Story.get_by_id_or_404(story_id)

    return render_template("story/story_index.jinja2", story=story)
