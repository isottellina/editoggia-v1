# test_commands.py ---
#
# Filename: test_commands.py
# Author: Louise <louise>
# Created: Sun Jun 21 19:37:24 2020 (+0200)
# Last-Updated: Wed Jun 24 11:30:34 2020 (+0200)
#           By: Louise <louise>
#
import flask_migrate
import pytest
from unittest import TestCase

from editoggia.database import db

from editoggia.models import User, Role
from editoggia.models import Story

from editoggia.commands import populate_db_users, populate_db_stories
from editoggia.commands import populate_db, set_admin

@pytest.mark.usefixtures("transaction")
class TestCommands(TestCase):
    """
    Tests the commands. They mostly have only one course
    of action.
    """

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
        populate_db_users(1)

        admin_role = db.session.query(Role).filter(Role.name == "Administrator").first()
        user = db.session.query(User).first()

        set_admin(user.username)

        self.assertIn(admin_role, user.roles)
