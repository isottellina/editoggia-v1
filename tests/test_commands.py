# test_commands.py --- 
# 
# Filename: test_commands.py
# Author: Louise <louise>
# Created: Sun Jun 21 19:37:24 2020 (+0200)
# Last-Updated: Mon Jun 22 19:07:57 2020 (+0200)
#           By: Louise <louise>
# 
from flask_testing import TestCase

from editoggia import create_app
from editoggia.database import db

from editoggia.models import User, Role, Permission, FandomCategory
from editoggia.models import Story, Chapter

from editoggia.commands import create_db, populate_db_users, populate_db_stories
from editoggia.commands import populate_db, set_admin

class TestCommands(TestCase):
    """
    Tests the commands. They mostly have only one course
    of action.
    """
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

    def test_populate_db_users(self):
        """
        Tests the populate_db_users command.
        """
        populate_db_users(5)

        users = db.session.query(User).all()

        self.assertEqual(len(users), 5)

    def test_populate_db_stories(self):
        """
        Tests the populate_db_stories command.
        We have to launch create_db because if
        not, there would be no fandoms. We also
        have to create users.
        """
        create_db()
        populate_db_users(1)
        populate_db_stories(5, 3)

        stories = db.session.query(Story).all()

        self.assertEqual(len(stories), 5)
        self.assertEqual(len(stories[0].chapters), 3)

    def test_populate_db(self):
        """
        Tests the populate_db command.
        We have to create_db.
        """
        create_db()
        populate_db(num_users=5, num_stories=5, num_chapters=3)

        users = db.session.query(User).all()
        stories = db.session.query(Story).all()

        self.assertEqual(len(users), 5)
        self.assertEqual(len(stories), 5)
        self.assertEqual(len(stories[0].chapters), 3)
        
    def test_set_admin(self):
        """
        Tests the set_admin command.
        """
        create_db()
        populate_db_users(1)

        admin_role = db.session.query(Role) \
                               .filter(Role.name == "Administrator") \
                               .first()
        user = db.session.query(User).first()
        
        set_admin(user.username)

        self.assertIn(admin_role, user.roles)
