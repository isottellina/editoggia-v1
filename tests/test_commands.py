# test_commands.py --- 
# 
# Filename: test_commands.py
# Author: Louise <louise>
# Created: Sun Jun 21 19:37:24 2020 (+0200)
# Last-Updated: Sun Jun 21 21:43:35 2020 (+0200)
#           By: Louise <louise>
# 
from flask_testing import TestCase

from editoggia import create_app
from editoggia.database import db
from editoggia.models import Role, Permission, FandomCategory, Story, Chapter
from editoggia.commands import create_db, populate_db_users, populate_db_stories
from editoggia.commands import set_admin

class TestCommands(TestCase):
    def create_app(self):
        return create_app("testing")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_db(self):
        """
        Tests the create_db function.
        """
        create_db()

        roles = db.session.query(Role).all()
        perms = db.session.query(Permission).all()
        categories = db.session.query(FandomCategory).all()
        
        self.assertEqual(roles[0].name, "Administrator")
        self.assertEqual(roles[1].name, "Moderator")
        self.assertEqual(roles[0].permissions, perms)
        self.assertTrue(len(categories) >= 1)
