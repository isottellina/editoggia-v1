# admin.py --- 
# 
# Filename: admin.py
# Author: Louise <louise>
# Created: Sat May  9 19:16:22 2020 (+0200)
# Last-Updated: Mon May 11 21:11:47 2020 (+0200)
#           By: Louise <louise>
# 
from app.admin import EditoggiaModelView, admin
from app.database import db
from app.user.models import User, Role, Permission

admin.add_view(EditoggiaModelView(User,
                                  db.session,
                                  category="User",
                                  endpoint='admin_user')
)

admin.add_view(EditoggiaModelView(Role,
                                  db.session,
                                  category="User",
                                  endpoint='admin_role')
)

admin.add_view(EditoggiaModelView(Permission,
                                  db.session,
                                  category="User",
                                  endpoint='admin_permission')
)
