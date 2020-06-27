# autocomplete.py --- 
# 
# Filename: autocomplete.py
# Author: Louise <louise>
# Created: Fri Jun  5 11:35:08 2020 (+0200)
# Last-Updated: Sat Jun 27 16:58:08 2020 (+0200)
#           By: Louise <louise>
# 
from flask import request, jsonify, abort
from flask_login import current_user

from sqlalchemy import func

from editoggia.ajax import ajax
from editoggia.ajax.forms import LikeForm

from editoggia.database import db
from editoggia.models import Fandom, Tag, FandomStories, StoryTags

@ajax.route('/autocomplete/<model_name>')
def autocomplete(model_name):
    """
    Returns the 20 most popular model_name.
    """
    query = request.args.get('q', '')

    if model_name == "Fandom":
        count_stmt = db.session.query(FandomStories.fandom_id,
                                      func.count('*').label('story_count')
        ).group_by(FandomStories.fandom_id).subquery()
        results = db.session.query(Fandom.name) \
                            .outerjoin(count_stmt, Fandom.id==count_stmt.c.fandom_id) \
                            .filter(Fandom.name.ilike(f'{query}%')) \
                            .order_by(count_stmt.c.story_count.desc())[:20]
    elif model_name == "Tag":
        count_stmt = db.session.query(StoryTags.tag_id,
                                      func.count('*').label('story_count')
        ).group_by(StoryTags.tag_id).subquery()
        results = db.session.query(Tag.name) \
                            .outerjoin(count_stmt, Tag.id==count_stmt.c.tag_id) \
                            .filter(Tag.name.ilike(f'{query}%')) \
                            .order_by(count_stmt.c.story_count.desc())[:20]
    else:
        abort(400)

    print(results)
    return jsonify(
        results=[
            {"id": result[0], "text": result[0]}
            for n, result in enumerate(results)
        ]
    )
