# test_moderation.py ---
#
# Filename: test_moderation.py
# Author: Louise <louise>
# Created: Sat Jul 11 23:30:29 2020 (+0200)
# Last-Updated: Sat Jul 11 23:46:47 2020 (+0200)
#           By: Louise <louise>
#
"""
These tests test the moderation blueprint.
"""
from editoggia.database import db
from editoggia.models import Fandom, Tag

from helpers import EditoggiaTestCase


class TestModeration(EditoggiaTestCase):
    """
    Tests the moderation views.
    """

    def test_permission(self):
        """
        Tests we can't access the views without permissions.
        """
        rv = self.client.get("/moderation/")

        self.assert403(rv)

    def test_can_access(self):
        """
        With the permission, we can access it.
        """
        self.login()
        rv = self.client.get("/moderation/")

        self.assert200(rv)

    def test_fandoms_get(self):
        """
        Tests we get the correct list of fandoms
        """
        # Create a fandom first
        fandom = Fandom.create(name="Disney", waiting_mod=True)

        self.login()
        rv = self.client.get("/moderation/fandoms")

        self.assertStatus(rv, 200)
        self.assertIn(b"Disney", rv.data)

    def test_fandoms_post(self):
        """
        Tests we can attribute a category to a fandom.
        """
        # Create a fandom first
        fandom = Fandom.create(name="Disney", waiting_mod=True)

        self.login()
        rv = self.client.post(
            "/moderation/fandoms",
            data={
                "fandoms-0-id": fandom.id,
                "fandoms-0-name": fandom.name,
                "fandoms-0-category": "Other",
            },
        )

        self.assertStatus(rv, 302)
        self.assertEqual(fandom.category.name, "Other")
        self.assertEqual(fandom.waiting_mod, False)

    def test_tags_get(self):
        """
        Tests we can get the list of tags.
        """
        # Create a fandom first
        tag = Tag.create(name="Slow Burn", waiting_mod=True)

        self.login()
        rv = self.client.get("/moderation/tags")

        self.assertStatus(rv, 200)
        self.assertIn(b"Slow Burn", rv.data)

    def test_tags_post(self):
        """
        Tests we can set a tag.
        """
        # Create a fandom first
        tag = Tag.create(name="Slow Burn", waiting_mod=True)

        self.login()
        rv = self.client.post(
            "/moderation/tags",
            data={
                "tags-0-id": tag.id,
                "tags-0-name": tag.name,
            },
        )

        self.assertStatus(rv, 302)
        self.assertEqual(tag.waiting_mod, False)
