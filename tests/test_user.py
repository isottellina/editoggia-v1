# test_user.py --- 
# 
# Filename: test_user.py
# Author: Louise <louise>
# Created: Fri May  8 20:30:10 2020 (+0200)
# Last-Updated: Sat May  9 20:09:31 2020 (+0200)
#           By: Louise <louise>
#
"""
These tests test both the user blueprint and the auth blueprint.
"""
from app import create_app
from app.database import db
from app.users.models import User

from faker import Faker
import unittest

fake = Faker()

class TestUser(unittest.TestCase):
    def setUp(self):
        app = create_app("testing")
        db.app = app
        db.create_all()
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def register(self, username, email, password):
        """
        Helper function to register an user.
        """
        return self.app.post('/signup', data={
            "username": username,
            "email": email,
            "password": password,
            "confirm": password
        }, follow_redirects=True)

    def test_signup_normal(self):
        """
        Tests that the user can sign up.
        """
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        
        rv = self.register(username, email, password)

        assert rv._status_code == 200
        assert b"Signed-up user" in rv.data

        # Check the user exists in the database
        assert db.session.query(
            User.query.filter(User.username == username).exists()
        ).scalar()

    def test_signup_short_username(self):
        """
        Tests that a 1-character username is refused.
        """
        username = 'a'
        email = fake.email()
        password = fake.password()

        rv = self.register(username, email, password)

        assert rv._status_code == 200
        assert b"Username must be between 2 and 50 characters." in rv.data

        # Check the user does not exist in the database
        assert not db.session.query(
            User.query.filter(User.username == username).exists()
        ).scalar()
        
    def test_signup_bad_email(self):
        """
        Tests that a bad email is refused.
        """
        username = fake.user_name()
        email = "badmail"
        password = fake.password()

        rv = self.register(username, email, password)

        assert rv._status_code == 200
        assert b"Email must be valid." in rv.data

        # Check the user does not exist in the database
        assert not db.session.query(
            User.query.filter(User.username == username).exists()
        ).scalar()

    def test_signup_empty_email(self):
        """
        Tests that an empty email is refused.
        """
        username = fake.user_name()
        email = ""
        password = fake.password()

        rv = self.register(username, email, password)

        assert rv._status_code == 200
        assert b"Email must be filled." in rv.data

        # Check the user does not exist in the database
        assert not db.session.query(
            User.query.filter(User.username == username).exists()
        ).scalar()

    def test_signup_empty_email(self):
        """
        Tests that an email longer than 128 is refused.
        """
        username = fake.user_name()
        email = "{}@gmail.com".format('a' * 128)
        password = fake.password()

        rv = self.register(username, email, password)

        assert rv._status_code == 200
        assert b"Email must be less than 128 characters." in rv.data

        # Check the user does not exist in the database
        assert not db.session.query(
            User.query.filter(User.username == username).exists()
        ).scalar()

    def test_signup_bad_confirm_password(self):
        """
        Tests that the confirm password field is checked. With this
        test, we normally have tested all the validators used, and
        thus, should be good to go.
        """
        username = fake.user_name()
        email = fake.email()
        password = fake.password()

        # We have to do this request ourselves since
        # the helper functions abstracts the confirm
        # password field for us.
        rv = self.app.post('/signup', data={
            "username": username,
            "email": email,
            "password": password,
            "confirm": password[:len(password) // 2]
        }, follow_redirects=True)

        assert rv._status_code == 200
        assert b"Passwords must match." in rv.data

        # Check the user does not exist in the database
        assert not db.session.query(
            User.query.filter(User.username == username).exists()
        ).scalar()
