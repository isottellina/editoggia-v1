# autocomplete.py --- 
# 
# Filename: autocomplete.py
# Author: Louise <louise>
# Created: Fri Jun  5 11:35:08 2020 (+0200)
# Last-Updated: Thu Jun 11 15:59:18 2020 (+0200)
#           By: Louise <louise>
# 
from flask import request, jsonify
from flask_login import current_user

from editoggia.ajax import ajax
from editoggia.ajax.decorators import ajax_login_required
from editoggia.ajax.forms import LikeForm

from editoggia.database import db
from editoggia.models import Fandom, Tag

@ajax.route('/autocomplete/<model_name>')
def autocomplete(model_name):
    """
    Returns the 20 most popular model_name.
    """
    models = {
        "Fandom": Fandom,
        "Tag": Tag
    }

    if model_name not in models:
        abort(400)
    model = models[model_name]
    
    return jsonify(
        results=[]
    )
