# interaction.py --- 
# 
# Filename: interaction.py
# Author: Louise <louise>
# Created: Sat Jun 27 13:58:01 2020 (+0200)
# Last-Updated: Sat Jun 27 14:05:52 2020 (+0200)
#           By: Louise <louise>
# 
"""
This file defines views for interaction, such as like, or comment.
"""
import bleach

from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from editoggia.database import db
from editoggia.models import Story, Chapter

from editoggia.story import story
from editoggia.story.forms import CommentForm, LikeForm
