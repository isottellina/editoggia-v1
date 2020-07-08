# test_user.py ---
#
# Filename: test_user.py
# Author: Louise <louise>
# Created: Fri May  8 20:30:10 2020 (+0200)
# Last-Updated: Sat May 30 15:21:02 2020 (+0200)
#           By: Louise <louise>
#
"""
These tests test the auth blueprint.
"""
from editoggia.database import db
from editoggia.models import User

from helpers import EditoggiaTestCase

class TestAuth(EditoggiaTestCase):
    #
    # Register tests
    #
    def register(self, username, email, password):
        """
        Helper function to register an user.
        """
        return self.client.post('/signup', data={
            "username": username,
            "email": email,
            "password": password,
            "confirm": password
        }, follow_redirects=True)

    def user_exists(self, username):
        """
        Returns true if a given user exists in the database.
        """
        return db.session.query(
            User.query.filter(User.username == username).exists()
        ).scalar()

    def test_signup_normal(self):
        """
        Tests that the user can sign up.
        """
        username = self.faker.user_name()
        email = self.faker.email()
        password = self.faker.password()

        rv = self.register(username, email, password)

        self.assert200(rv)
        self.assertIn(b"Signed-up user", rv.data)

        # Check the user exists in the database
        self.assertTrue(self.user_exists(username))

    def test_signup_short_username(self):
        """
        Tests that a 1-character username is refused.
        """
        username = 'a'
        email = self.faker.email()
        password = self.faker.password()

        rv = self.register(username, email, password)

        self.assert200(rv)
        self.assertIn(b"Username must be between 2 and 50 characters.", rv.data)

        # Check the user does not exist in the database
        self.assertFalse(self.user_exists(username))

    def test_signup_short_username(self):
        """
        Tests that an username containing non-alphanumerical
        characters is refused.
        """
        username = 'user/mountain'
        email = self.faker.email()
        password = self.faker.password()

        rv = self.register(username, email, password)

        self.assert200(rv)
        self.assertIn(b"Username can only contain alphanumerical characters.", rv.data)

        # Check the user does not exist in the database
        self.assertFalse(self.user_exists(username))

    def test_signup_bad_email(self):
        """
        Tests that a bad email is refused.
        """
        username = self.faker.user_name()
        email = "badmail"
        password = self.faker.password()

        rv = self.register(username, email, password)

        self.assert200(rv)
        self.assertIn(b"Email must be valid.", rv.data)

        # Check the user does not exist in the database
        self.assertFalse(self.user_exists(username))

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
        self.assertFalse(self.user_exists(username))

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
        self.assertFalse(self.user_exists(username))

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
        rv = self.client.post('/signup', data={
            "username": username,
            "email": email,
            "password": password,
            "confirm": password[:len(password) // 2]
        }, follow_redirects=True)

        self.assert200(rv)
        self.assertIn(b"Passwords must match.", rv.data)

        # Check the user does not exist in the database
        self.assertFalse(self.user_exists(username))

    def test_username_already_registered(self):
        """
        Tests that the app refuses to register another user
        with the same username.
        """
        email = self.faker.email()
        password = self.faker.password()

        rv = self.register(self.user.username, email, password)

        self.assert200(rv)
        self.assertIn(b"Username already registered.", rv.data)

    def test_email_already_registered(self):
        """
        Tests that the app refuses to register another user
        with the same email
        """
        username = self.faker.user_name()
        password = self.faker.password()

        rv = self.register(username, self.user.email, password)

        self.assert200(rv)
        self.assertIn(b"Email already registered.", rv.data)

        # Check the second user does not exist in the database
        self.assertFalse(self.user_exists(username))

    #
    # Login tests
    #

    def test_login_normal(self):
        """
        Tests that we can log in with the user.
        """
        rv = self.login(self.user.username, self.password)

        self.assert200(rv)
        self.assertIn(b"You were logged in as", rv.data)
        self.assertIn(self.user.name.encode('utf8'), rv.data)

    def test_login_missing_data(self):
        """
        Tests that we cannot login without supplying all data.
        """
        rv = self.login(self.user.username, "")

        self.assert200(rv)
        self.assertNotIn(b"You were logged in as", rv.data)
        self.assertIn(b"Password must be filled.", rv.data)

    def test_login_username_must_exist(self):
        """
        Tests that we cannot log in as an user that doesn't exist.
        """
        rv = self.login(self.user.username + "2", self.password)

        self.assert200(rv)
        self.assertNotIn(b"You were logged in as", rv.data)
        self.assertIn(b"Unknown username.", rv.data)

    def test_login_password_must_be_correct(self):
        """
        Tests that we cannot log in with a bad password
        """
        rv = self.login(self.user.username,
                        self.password[:len(self.password) // 2])

        self.assert200(rv)
        self.assertNotIn(b"You were logged in as", rv.data)
        self.assertIn(b"Invalid password.", rv.data)

    #
    # Log out tests
    #
    def test_logout_normal(self):
        """
        Tests that we can log out
        """
        self.login(self.user.username, self.password)
        rv = self.client.get('/logout', follow_redirects=True)

        self.assert200(rv)
        self.assertIn(b"You were logged out", rv.data)
