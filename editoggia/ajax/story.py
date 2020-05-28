# story.py --- 
# 
# Filename: story.py
# Author: Louise <louise>
# Created: Thu May 28 15:56:24 2020 (+0200)
# Last-Updated: Thu May 28 16:07:54 2020 (+0200)
#           By: Louise <louise>
#
from flask_login import current_user

from editoggia.ajax import ajax
from editoggia.ajax.decorators import ajax_login_required

@ajax.route('/story/like')
@ajax_login_required
def story_like():
    return "", 200
