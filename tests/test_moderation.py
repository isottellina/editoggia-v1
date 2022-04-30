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

    def test_permission(self, client):
        """
        Tests we can't access the views without permissions.
        """
        rv = client.get("/moderation/")

        assert rv.status_code == 403

    def test_can_access(self, app, create_user):
        """
        With the permission, we can access it.
        """
        user, _ = create_user(is_admin=True)

        with app.test_client(user=user) as client:
            rv = client.get("/moderation/")
        assert rv.status_code == 200

    def test_fandoms_get(self, app, create_user):
        """
        Tests we get the correct list of fandoms
        """
        user, _ = create_user(is_admin=True)
        # Create a fandom first
        fandom = Fandom.create(name="Disney", waiting_mod=True)

        with app.test_client(user=user) as client:
            rv = client.get("/moderation/fandoms")

        assert rv.status_code == 200
        assert fandom.name.encode() in rv.data

    def test_fandoms_post(self, app, create_user):
        """
        Tests we can attribute a category to a fandom.
        """
        user, _ = create_user(is_admin=True)

        # Create a fandom first
        fandom = Fandom.create(name="Disney", waiting_mod=True)

        with app.test_client(user=user) as client:
            rv = client.post(
                "/moderation/fandoms",
                data={
                    "fandoms-0-id": fandom.id,
                    "fandoms-0-name": fandom.name,
                    "fandoms-0-category": "Other",
                },
            )

        assert rv.status_code < 400
        assert fandom.category.name == "Other"
        assert not fandom.waiting_mod

    def test_tags_get(self, app, create_user):
        """
        Tests we can get the list of tags.
        """
        user, _ = create_user(is_admin=True)
        tag = Tag.create(name="Slow Burn", waiting_mod=True)

        with app.test_client(user=user) as client:
            rv = client.get("/moderation/tags")

        assert rv.status_code == 200
        assert tag.name.encode() in rv.data

    def test_tags_post(self, app, create_user):
        """
        Tests we can set a tag.
        """
        user, _ = create_user(is_admin=True)
        tag = Tag.create(name="Slow Burn", waiting_mod=True)

        with app.test_client(user=user) as client:
            rv = client.post(
                "/moderation/tags",
                data={
                    "tags-0-id": tag.id,
                    "tags-0-name": tag.name,
                },
            )

        assert rv.status_code < 400
        assert not tag.waiting_mod
