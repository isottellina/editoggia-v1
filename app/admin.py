# admin.py --- 
# 
# Filename: admin.py
# Author: Louise <louise>
# Created: Sat May  9 19:25:47 2020 (+0200)
# Last-Updated: Sat May  9 19:30:33 2020 (+0200)
#           By: Louise <louise>
# 
"""
Creates the Admin blueprint, and helpers for
views within the Admin interface.
"""
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin

admin = Admin(
    name='Editoggia',
    template_mode='bootstrap3'
)

# A helper class to assess if a user can access the admin view
class EditoggiaModelView(ModelView):
    def is_accessible(self):
        """
        TODO: Return a real value here, admins should be able to
        access these views.
        """
        return False
