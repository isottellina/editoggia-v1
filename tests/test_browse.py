# test_browse.py ---
#
# Filename: test_browse.py
# Author: Louise <louise>
# Created: Fri Jun 26 19:38:42 2020 (+0200)
# Last-Updated: Sun Jul 12 00:06:25 2020 (+0200)
#           By: Louise <louise>
#
from helpers import EditoggiaTestCase

from editoggia.database import db
from editoggia.models import Story, Fandom, Tag


class TestBrowse(EditoggiaTestCase):
    def test_fandoms(self, client):
        """
        Tests the fandoms view, printing all fandoms in a category.
        """
        rv = client.get("/browse/fandoms/Other")

        assert rv.status_code == 200
        assert b"Original Work" in rv.data

    def test_collection_title(self, client, create_story):
        """
        Tries to display stories in order of title.
        """
        stories = [create_story() for _ in range(2)]

        least_title = min(stories[0].title, stories[1].title)
        most_title = max(stories[0].title, stories[1].title)

        rv = client.get("/browse/fandom/Original Work?order_by=title")
        assert rv.status_code == 200
        assert rv.data.find(least_title.encode()) < rv.data.find(most_title.encode())

    def test_collection_author(self, client, create_user, create_story):
        """
        Tries to display stories in order of title.
        """
        user0, _ = create_user()
        user1, _ = create_user(user0.username + "2")

        least_author = create_story(author=user0)
        most_author = create_story(author=user1)

        rv = client.get("/browse/fandom/Original Work?order_by=author")
        assert rv.status_code == 200
        assert rv.data.find(least_author.title.encode()) < rv.data.find(most_author.title.encode())

    def test_collection_date_updated(self, client, create_story):
        """
        Tries to display stories in order of dates.
        """
        stories = [create_story() for _ in range(2)]

        rv = client.get("/browse/fandom/Original Work")
        assert rv.status_code == 200
        assert rv.data.find(stories[1].title.encode()) < rv.data.find(stories[0].title.encode())

    def test_collection_hits(self, client, create_user, create_story):
        """
        Tries to display stories in order of hits.
        """
        user, _ = create_user()
        stories = [create_story() for _ in range(2)]
        self.hit(user, stories[0])

        rv = client.get("/browse/fandom/Original Work?order_by=hits")
        assert rv.status_code == 200
        assert rv.data.find(stories[0].title.encode()) < rv.data.find(stories[1].title.encode())

    def test_collection_likes(self, client, create_user, create_story):
        """
        Tries to display stories in order of likes.
        """
        user, _ = create_user()
        stories = [create_story() for _ in range(2)]
        self.like(user, stories[0])

        rv = client.get("/browse/fandom/Original Work?order_by=likes")
        assert rv.status_code == 200
        assert rv.data.find(stories[0].summary.encode()) < rv.data.find(stories[1].summary.encode())

    def test_collection_bad_order(self, client):
        """
        Bad ordering.
        """
        rv = client.get("/browse/fandom/Original Work?order_by=bad")
        assert rv.status_code == 400

    def test_collection_rating(self, client, create_story):
        """
        Tests we only get stories rated as we asked.
        """
        stories = [create_story() for _ in range(2)]

        # Set rating
        stories[1].update(rating="Explicit")

        rv = client.get("/browse/fandom/Original Work?rating=Explicit")

        assert rv.status_code == 200
        assert stories[0].title.encode() not in rv.data
        assert stories[1].title.encode() in rv.data

    def test_collection_included_fandoms(self, client, create_story):
        """
        Tests we can include another fandom in the search and only get
        twice-tagged stories.
        """
        other_fandom = Fandom.create(name="Fandom2")
        stories = [create_story() for _ in range(2)]

        # Add fandom to story
        stories[1].fandom.append(other_fandom)

        rv = client.get("/browse/fandom/Original Work?included_fandom=Fandom2")

        assert rv.status_code == 200
        assert stories[0].title.encode() not in rv.data
        assert stories[1].title.encode() in rv.data

    def test_collection_included_tags(self, client, create_story):
        """
        Tests we can include a tag in the search and only get stories
        tagged with it.
        """
        other_tag = Tag.create(name="Tag1")
        stories = [create_story() for _ in range(2)]

        # Add tag to story
        stories[1].update(tags=[other_tag])

        rv = client.get("/browse/fandom/Original Work?included_tags=Tag1")

        assert rv.status_code == 200
        assert stories[0].title.encode() not in rv.data
        assert stories[1].title.encode() in rv.data

    def test_collection_excluded_tags(self, client, create_story):
        """
        Tests we can exclude a tag in the search and only get stories
        that don't have it
        """
        other_tag = Tag.create(name="Tag1")
        stories = [create_story() for _ in range(2)]

        # Add tag to story
        stories[1].update(tags=[other_tag])

        rv = client.get("/browse/fandom/Original Work?excluded_tags=Tag1")

        assert rv.status_code == 200
        assert stories[0].title.encode() in rv.data
        assert stories[1].title.encode() not in rv.data
