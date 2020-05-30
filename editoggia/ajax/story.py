# story.py --- 
# 
# Filename: story.py
# Author: Louise <louise>
# Created: Thu May 28 15:56:24 2020 (+0200)
# Last-Updated: Sat May 30 15:57:19 2020 (+0200)
#           By: Louise <louise>
#
from flask import request
from flask_login import current_user

from editoggia.ajax import ajax
from editoggia.ajax.decorators import ajax_login_required
from editoggia.ajax.forms import LikeForm

from editoggia.database import db
from editoggia.models import Story, Chapter, Comment

@ajax.route('/story/like', methods=['POST'])
@ajax_login_required
def story_like():
    form = LikeForm()

    if form.validate_on_submit():
        story = Story.get_by_id(form.data['story'])
        
        # TODO: Add validator to do that
        if story is None:
            return jsonify(
                message="Story doesn't exist"
            ), 404

        # If the story is not already liked, like it
        if story not in current_user.likes:
            current_user.likes.append(story)
        else:
            current_user.likes.remove(story)

        db.session.commit()
        
        return "", 200

@ajax.route('/story/post_comment', methods=['POST'])
@ajax_login_required
def post_comment():
    form = CommentForm()

    if form.validate_on_submit():
        chapter = Chapter.get_by_id(form.data['chapter'])
        
        # TODO: Add validator to do that
        if chapter is None:
            return jsonify(
                message="Chapter doesn't exist"
            ), 404

        # Bleach the content
        content = bleach.clean(form.data['content'])
        
        Comment.create(
            content=content,
            author=current_user,
            chapter=chapter
        )
        
        return "", 200
