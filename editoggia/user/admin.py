# admin.py ---
#
# Filename: admin.py
# Author: Louise <louise>
# Created: Sat May  9 19:16:22 2020 (+0200)
# Last-Updated: Wed Jul  8 11:48:14 2020 (+0200)
#           By: Louise <louise>
#
from editoggia.admin import EditoggiaModelView, admin
from editoggia.database import db
from editoggia.models import User, Role, Permission


class UserView(EditoggiaModelView):
    """
    Exclude password hash from viewable columns.
    """

    column_exclude_list = ["pw_hash"]


admin.add_view(UserView(User, db.session, category="User", endpoint="admin_user"))

admin.add_view(
    EditoggiaModelView(Role, db.session, category="User", endpoint="admin_role")
)

admin.add_view(
    EditoggiaModelView(
        Permission, db.session, category="User", endpoint="admin_permission"
    )
)
