# test_user.py --- 
# 
# Filename: test_user.py
# Author: Louise <louise>
# Created: Fri May  8 20:30:10 2020 (+0200)
# Last-Updated: Fri May 15 21:47:20 2020 (+0200)
#           By: Louise <louise>
#
"""
These tests test the auth blueprint.
"""
from app.database import db
from app.user.models import User

from helpers import EditoggiaTestCase

class TestAuth(EditoggiaTestCase):
    #
    # Register tests
    #
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

    def login(self, username, password):
        """
        Helper function to login as an user.
        """
        return self.app.post('/login', data={
            "username": username,
            "password": password
        }, follow_redirects=True)

    def test_signup_normal(self):
        """
        Tests that the user can sign up.
        """
        username = self.faker.user_name()
        email = self.faker.email()
        password = self.faker.password()
        
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
        email = self.faker.email()
        password = self.faker.password()

        rv = self.register(username, email, password)

        assert rv._status_code == 200
        assert b"Username must be between 2 and 50 characters." in rv.data

        # Check the user does not exist in the database
        assert not db.session.query(
            User.query.filter(User.username == username).exists()
        ).scalar()

    def test_signup_short_username(self):
        """
        Tests that an username containing non-alphanumerical
        characters is refused.
        """
        username = 'user/mountain'
        email = self.faker.email()
        password = self.faker.password()

        rv = self.register(username, email, password)

        assert rv._status_code == 200
        assert b"Username can only contain alphanumerical characters." in rv.data

        # Check the user does not exist in the database
        assert not db.session.query(
            User.query.filter(User.username == username).exists()
        ).scalar()
        
    def test_signup_bad_email(self):
        """
        Tests that a bad email is refused.
        """
        username = self.faker.user_name()
        email = "badmail"
        password = self.faker.password()

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
        username = self.faker.user_name()
        email = ""
        password = self.faker.password()

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
        username = self.faker.user_name()
        email = "{}@gmail.com".format('a' * 128)
        password = self.faker.password()

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
        username = self.faker.user_name()
        email = self.faker.email()
        password = self.faker.password()

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

    def test_username_already_registered(self):
        """
        Tests that the app refuses to register another user
        with the same username.
        """
        email = self.faker.email()
        password = self.faker.password()

        rv = self.register(self.user.username, email, password)
        
        assert rv._status_code == 200
        assert b"Username already registered." in rv.data

    def test_email_already_registered(self):
        """
        Tests that the app refuses to register another user
        with the same email
        """
        username = self.faker.user_name()
        password = self.faker.password()

        rv = self.register(username, self.user.email, password)
        
        assert rv._status_code == 200
        assert b"Email already registered." in rv.data

        # Check the second user does not exist in the database
        assert not db.session.query(
            User.query.filter(User.username == username).exists()
        ).scalar()

    #
    # Login tests
    #
    
    def test_login_normal(self):
        """
        Tests that we can log in with the user.
        """
        rv = self.login(self.user.username, self.password)

        assert rv._status_code == 200
        assert b"You were logged in as" in rv.data
        assert self.user.name.encode('utf8') in rv.data

    def test_login_missing_data(self):
        """
        Tests that we cannot login without supplying all data.
        """
        rv = self.login(self.user.username, "")

        assert rv._status_code == 200
        assert b"You were logged in as" not in rv.data
        assert b"Password must be filled." in rv.data

    def test_login_username_must_exist(self):
        """
        Tests that we cannot log in as an user that doesn't exist.
        """
        rv = self.login(self.user.username + "2", self.password)

        assert rv._status_code == 200
        assert b"You were logged in as" not in rv.data
        assert b"Unknown username." in rv.data

    def test_login_password_must_be_correct(self):
        """
        Tests that we cannot log in with a bad password
        """
        rv = self.login(self.user.username,
                        self.password[:len(self.password) // 2])

        assert rv._status_code == 200
        assert b"You were logged in as" not in rv.data
        assert b"Invalid password." in rv.data

    #
    # Log out tests
    #
    def test_logout_normal(self):
        """
        Tests that we can log out
        """
        self.login(self.user.username, self.password)
        rv = self.app.get('/logout', follow_redirects=True)

        assert rv._status_code == 200
        assert b"You were logged out" in rv.data
