# admin.py --- 
# 
# Filename: admin.py
# Author: Louise <louise>
# Created: Sat May  9 19:16:22 2020 (+0200)
# Last-Updated: Sat May  9 19:28:52 2020 (+0200)
#           By: Louise <louise>
# 
from app.admin import EditoggiaModelView, admin
from app.database import db
from app.users.models import User, Role, Permission

admin.add_view(EditoggiaModelView(User, db.session))
admin.add_view(EditoggiaModelView(Role, db.session))
admin.add_view(EditoggiaModelView(Permission, db.session))
