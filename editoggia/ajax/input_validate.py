# input_validate.py --- 
# 
# Filename: input_validate.py
# Author: Louise <louise>
# Created: Thu May 28 22:00:26 2020 (+0200)
# Last-Updated: Thu May 28 22:43:04 2020 (+0200)
#           By: Louise <louise>
# 
from flask_inputs import Inputs
from flask_babel import gettext
from wtforms.validators import DataRequired

from editoggia.database import db
from editoggia.models.story import Story

class LikeInputs(Inputs):
    json = {
        "story": [
            DataRequired(
                message=gettext("The story parameter is needed.")
            )
        ]
    }
