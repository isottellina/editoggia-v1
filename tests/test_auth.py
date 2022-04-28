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
from faker.proxy import Faker
from editoggia.database import db
from editoggia.models import User

from helpers import EditoggiaTestCase


class TestAuth(EditoggiaTestCase):
    #
    # Register tests
    #
    def register(self, client, username, email, password):
        """
        Helper function to register an user.
        """
        return client.post(
            "/signup",
            data={
                "username": username,
                "email": email,
                "password": password,
                "confirm": password,
            },
            follow_redirects=True,
        )

    def user_exists(self, username):
        """
        Returns true if a given user exists in the database.
        """
        return db.session.query(
            User.query.filter(User.username == username).exists()
        ).scalar()

    def test_signup_normal(self, client):
        """
        Tests that the user can sign up.
        """
        username = self.faker.user_name()
        email = self.faker.email()
        password = self.faker.password()

        rv = self.register(client, username, email, password)

        assert rv.status_code == 200
        assert b"Signed-up user" in rv.data
        assert self.user_exists(username)

    def test_signup_short_username(self, client):
        """
        Tests that a 1-character username is refused.
        """
        username = "a"
        email = self.faker.email()
        password = self.faker.password()

        rv = self.register(client, username, email, password)

        assert rv.status_code == 200
        assert b"Username must be between 2 and 50 characters." in rv.data
        assert not self.user_exists(username)

    def test_signup_bad_username(self, client):
        """
        Tests that an username containing non-alphanumerical
        characters is refused.
        """
        username = "user/mountain"
        email = self.faker.email()
        password = self.faker.password()

        rv = self.register(client, username, email, password)

        assert rv.status_code == 200
        assert b"Username can only contain alphanumerical characters." in rv.data
        assert not self.user_exists(username)

    def test_signup_bad_email(self, client):
        """
        Tests that a bad email is refused.
        """
        username = self.faker.user_name()
        email = "badmail"
        password = self.faker.password()

        rv = self.register(client, username, email, password)

        assert rv.status_code == 200
        assert b"Email must be valid." in rv.data
        assert not self.user_exists(username)

    def test_signup_empty_email(self, client):
        """
        Tests that an empty email is refused.
        """
        username = self.faker.user_name()
        email = ""
        password = self.faker.password()

        rv = self.register(client, username, email, password)

        assert rv._status_code == 200
        assert b"Email must be filled." in rv.data
        assert not self.user_exists(username)

    def test_signup_long_email(self, client):
        """
        Tests that an email longer than 128 is refused.
        """
        username = self.faker.user_name()
        email = "{}@gmail.com".format("a" * 128)
        password = self.faker.password()

        rv = self.register(client, username, email, password)

        assert rv._status_code == 200
        assert b"Email must be less than 128 characters." in rv.data
        assert not self.user_exists(username)

    def test_signup_bad_confirm_password(self, client):
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
        rv = client.post(
            "/signup",
            data={
                "username": username,
                "email": email,
                "password": password,
                "confirm": password[: len(password) // 2],
            },
            follow_redirects=True,
        )

        assert rv.status_code == 200
        assert b"Passwords must match." in rv.data
        assert not self.user_exists(username)

    def test_username_already_registered(self, client, user):
        """
        Tests that the app refuses to register another user
        with the same username.
        """
        email = self.faker.email()
        password = self.faker.password()

        rv = self.register(client, user.username, email, password)

        assert rv.status_code == 200
        assert b"Username already registered." in rv.data

    def test_email_already_registered(self, client, user):
        """
        Tests that the app refuses to register another user
        with the same email
        """
        username = self.faker.user_name()
        password = self.faker.password()

        rv = self.register(client, username, user.email, password)

        assert rv.status_code == 200
        assert b"Email already registered." in rv.data
        assert not self.user_exists(username)

    #
    # Login tests
    #

    def test_login_normal(self, client, user, password):
        """
        Tests that we can log in with the user.
        """
        rv = self.login(client, user.username, password)

        assert rv.status_code == 200
        assert b"You were logged in as" in rv.data
        assert user.name.encode("utf8") in rv.data

    def test_login_missing_data(self, client, user):
        """
        Tests that we cannot login without supplying all data.
        """
        rv = self.login(client, user.username, "")

        assert rv.status_code == 200
        assert b"You were logged in as" not in rv.data
        assert b"Password must be filled." in rv.data

    def test_login_username_must_exist(self, client, user, password):
        """
        Tests that we cannot log in as an user that doesn't exist.
        """
        rv = self.login(client, user.username + "2", password)

        assert rv.status_code == 200
        assert b"You were logged in as" not in rv.data
        assert b"Unknown username." in rv.data

    def test_login_password_must_be_correct(self, client, user, password):
        """
        Tests that we cannot log in with a bad password
        """
        rv = self.login(client, user.username, password[: len(password) // 2])

        assert rv.status_code == 200
        assert b"You were logged in as" not in rv.data
        assert b"Invalid password." in rv.data

    #
    # Log out tests
    #
    def test_logout_normal(self, client, user, password):
        """
        Tests that we can log out
        """
        self.login(client, user.username, password)
        rv = client.get("/logout", follow_redirects=True)

        assert rv.status_code == 200
        assert b"You were logged out", rv.data
