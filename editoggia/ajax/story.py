# story.py --- 
# 
# Filename: story.py
# Author: Louise <louise>
# Created: Thu May 28 15:56:24 2020 (+0200)
# Last-Updated: Thu May 28 23:02:38 2020 (+0200)
#           By: Louise <louise>
#
from flask import request
from flask_login import current_user

from editoggia.ajax import ajax
from editoggia.ajax.decorators import ajax_login_required, ajax_validate_data
from editoggia.ajax.input_validate import LikeInputs

from editoggia.database import db
from editoggia.models.story import Story

@ajax.route('/story/like', methods=['POST'])
@ajax_login_required
@ajax_validate_data(LikeInputs)
def story_like():
    story = Story.get_by_id(request.json['story'])

    # TODO: Add validator to do that
    if story is None:
        return jsonify(
            message="Story doesn't exist"
        ), 404
    
    story.user_likes.append(current_user)
    db.session.commit()

    return "", 200
