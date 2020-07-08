# admin.py ---
#
# Filename: admin.py
# Author: Louise <louise>
# Created: Sat May  9 19:25:47 2020 (+0200)
# Last-Updated: Tue May 12 21:20:32 2020 (+0200)
#           By: Louise <louise>
#
"""
Creates the Admin blueprint, and helpers for
views within the Admin interface.
"""
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin

admin = Admin(
    name='Editoggia',
    template_mode='bootstrap3'
)

class EditoggiaModelView(ModelView):
    """
    Helper class for ModelViews in the admin interface. The main
    goal of this class is to only allow logged-in users who have
    the permission to access it.
    """
    def is_accessible(self):
        """
        TODO: Return a real value here, admins should be able to
        access these views.
        """
        return current_user.has_permission("admin.ACCESS_ADMIN_INTERFACE")
