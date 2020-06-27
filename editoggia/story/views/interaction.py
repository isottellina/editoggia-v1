# interaction.py --- 
# 
# Filename: interaction.py
# Author: Louise <louise>
# Created: Sat Jun 27 13:58:01 2020 (+0200)
# Last-Updated: Sat Jun 27 15:54:08 2020 (+0200)
#           By: Louise <louise>
# 
"""
This file defines views for interaction, such as like, or comment.
"""
import bleach

from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from editoggia.database import db
from editoggia.models import Story, Chapter, Comment

from editoggia.story import story
from editoggia.story.forms import CommentForm, LikeForm

@story.route('/<int:story_id>/like', methods=["POST"])
@login_required
def like(story_id):
    """
    Like or unlike a story. Can only be accessed by POST.
    """
    form = LikeForm()
    story = Story.get_by_id_or_404(story_id)

    if form.validate_on_submit():
        # If the story is not already liked, like it
        # Else, remove it from the likes.
        if story not in current_user.likes:
            current_user.likes.append(story)
        else:
            current_user.likes.remove(story)

        db.session.commit()
        return "", 200
    else:
        return "", 400

@story.route('/<int:story_id>/chapter/<int:chapter_id>/comment', methods=["POST"])
@login_required
def comment(story_id, chapter_id):
    """
    Comment on a chapter. Can only POST too.
    """
    form = CommentForm()
    chapter = Chapter.get_by_id_or_404(chapter_id)

    if form.validate_on_submit():
        content = bleach.clean(form.data['comment'])
        
        Comment.create(
            content=content,
            author=current_user,
            chapter=chapter
        )
        return redirect(url_for('story.show_chapter', story_id=story_id, chapter_id=chapter_id))
    else:
        abort(400)
