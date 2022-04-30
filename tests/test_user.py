# test_user.py ---
#
# Filename: test_user.py
# Author: Louise <louise>
# Created: Fri May 15 21:41:06 2020 (+0200)
# Last-Updated: Tue Jul  7 16:50:11 2020 (+0200)
#           By: Louise <louise>
#
"""
These tests test the user blueprint.
"""
import datetime

import pytest
from helpers import EditoggiaTestCase


class TestUser(EditoggiaTestCase):
    """
    Test view profile.
    """

    def test_view_profile_doesnt_exist(self, client):
        """
        Tests that the app 404s when an user doesn't exist.
        """
        rv = client.get("/user/notexist")
        assert rv.status_code == 404

    def test_view_profile_normal(self, client, create_user):
        """
        Tests we can access a profile that exist.
        """
        user, _ = create_user()

        # We put a little info in the profile
        user.location = "Paris, France"
        user.birthdate = datetime.date(1995, 5, 3)

        age = (datetime.date.today() - user.birthdate) // datetime.timedelta(
            days=365.2425
        )

        # We get the URL to do the actual request
        rv = client.get(f"/user/{user.username}")

        assert rv.status_code == 200
        assert b"Paris, France" in rv.data
        assert str(age).encode() in rv.data

    def test_view_profile_normal_wo_birthdate(self, client, create_user):
        """
        Tests we can access a profile that exist, without birthdate.
        """
        user, _ = create_user()

        # We put a little info in the profile
        user.location = "Paris, France"

        # We get the URL to do the actual request
        rv = client.get(f"/user/{user.username}")

        assert rv.status_code == 200
        assert b"Paris, France" in rv.data
        assert b'id="age"' not in rv.data

    def test_view_profile_likes(self, client, create_user, create_story):
        """
        Tests we can access a profile's likes.
        """
        user, _ = create_user()

        story = create_story(user)
        self.like(user, story)

        rv = client.get(f"/user/{user.username}/liked")
        assert rv.status_code == 200
        assert story.title.encode() in rv.data

    def test_view_profile_history(self, client, create_user, create_story):
        """
        Tests we can access a profile's history.
        """
        user, _ = create_user()
        story = create_story(user)
        self.hit(user, story)

        # We get the URL to do the actual request
        rv = client.get(f"/user/{user.username}/history")
        assert rv.status_code == 200
        assert story.title.encode() in rv.data

    """
    Test edit profile.
    """

    def test_edit_get(self, client, create_user):
        """
        Tests that we get the form when we send a
        GET request.
        """
        user, password = create_user()
        self.login(client, user.username, password)
        rv = client.get("/user/edit")

        assert rv.status_code == 200
        assert b"<form" in rv.data
        assert f'value="{user.name}"'.encode() in rv.data

    @pytest.mark.parametrize("extra_data", [{}, {"birthdate": "1970-01-01"}])
    def test_edit_post(self, app, create_user, extra_data):
        user, _ = create_user()

        base_data = {
            "name": self.faker.name(),
            "email": self.faker.company_email(),
            "location": "Amsterdam, Netherlands",
            "gender": "Woman",
            "language": app.config["ACCEPTED_LANGUAGES"][0],
        }
        base_data.update(extra_data)

        with app.test_client(user=user) as client:
            _ = client.post("/user/edit", data=base_data)

        assert user.name == base_data["name"]
        assert user.email == base_data["email"]
        assert user.location == base_data["location"]
        assert user.gender == base_data["gender"]
        assert user.bio == ""
