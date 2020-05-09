# admin.py --- 
# 
# Filename: admin.py
# Author: Louise <louise>
# Created: Sat May  9 19:16:22 2020 (+0200)
# Last-Updated: Sat May  9 19:17:44 2020 (+0200)
#           By: Louise <louise>
# 
from flask_admin.contrib.sqla import ModelView

from app.extensions import admin
from app.database import db
from app.users.models import User, Role, Permission

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Permission, db.session))
