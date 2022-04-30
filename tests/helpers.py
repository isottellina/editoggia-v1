# helpers.py ---
#
# Filename: helpers.py
# Author: Louise <louise>
# Created: Fri May 15 21:42:56 2020 (+0200)
# Last-Updated: Sat Jul 11 23:34:06 2020 (+0200)
#           By: Louise <louise>
#
import pytest
from faker import Faker


@pytest.mark.usefixtures("transaction")
class EditoggiaTestCase:
    faker = Faker()

    def login(self, client, username, password):
        """
        Helper function to login as an user.
        If called without an argument, will login
        using parameters created during init.
        """
        return client.post(
            "/login",
            data={"username": username, "password": password},
            follow_redirects=True,
        )

    def hit(self, user, story, chapter_nb=1):
        """
        Add a hit of the story to user.
        """
        user.add_to_history(story, chapter_nb)

    def like(self, user, story):
        """
        Add story to stories liked by user user.
        """
        user.likes.append(story)
