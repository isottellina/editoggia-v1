# test_browse.py ---
#
# Filename: test_browse.py
# Author: Louise <louise>
# Created: Fri Jun 26 19:38:42 2020 (+0200)
# Last-Updated: Fri Jun 26 20:26:55 2020 (+0200)
#           By: Louise <louise>
#
from helpers import EditoggiaTestCase

from editoggia.database import db
from editoggia.models import Story, Fandom, Tag

class TestBrowse(EditoggiaTestCase):
    def test_fandoms(self):
        """
        Tests the fandoms view, printing all fandoms in a category.
        """
        rv = self.client.get('/browse/fandoms/Other')

        self.assert200(rv)
        self.assertIn(b'Original Work', rv.data)

    def test_collection_title(self):
        """
        Tries to display stories in order of title.
        """
        stories = self.create_stories(2)

        least_title = min(stories[0].title, stories[1].title)
        most_title = max(stories[0].title, stories[1].title)

        rv = self.client.get('/browse/fandom/Original Work?order_by=title')
        self.assert200(rv)
        self.assertTrue(rv.data.find(least_title.encode()) < rv.data.find(most_title.encode()))

    def test_collection_author(self):
        """
        Tries to display stories in order of title.
        """
        new_user, _ = self.create_user(self.user.username + "2")

        least_author = self.create_story()
        most_author = self.create_story(author=new_user)

        rv = self.client.get('/browse/fandom/Original Work?order_by=author')
        self.assert200(rv)
        self.assertTrue(rv.data.find(least_author.title.encode()) < rv.data.find(most_author.title.encode()))

    def test_collection_date_updated(self):
        """
        Tries to display stories in order of dates.
        """
        stories = self.create_stories(2)

        rv = self.client.get('/browse/fandom/Original Work')
        self.assert200(rv)
        self.assertTrue(rv.data.find(stories[1].title.encode()) < rv.data.find(stories[0].title.encode()))

    def test_collection_hits(self):
        """
        Tries to display stories in order of hits.
        """
        stories = self.create_stories(2)
        self.hit(stories[0])

        rv = self.client.get('/browse/fandom/Original Work?order_by=hits')
        self.assert200(rv)
        self.assertTrue(rv.data.find(stories[0].title.encode()) < rv.data.find(stories[1].title.encode()))

    def test_collection_likes(self):
        """
        Tries to display stories in order of likes.
        """
        stories = self.create_stories(2)
        self.like(stories[0])

        rv = self.client.get('/browse/fandom/Original Work?order_by=likes')
        self.assert200(rv)
        self.assertTrue(rv.data.find(stories[0].title.encode()) < rv.data.find(stories[1].title.encode()))

    def test_collection_bad_order(self):
        """
        Bad ordering.
        """
        stories = self.create_stories(2)

        rv = self.client.get('/browse/fandom/Original Work?order_by=bad')
        self.assert400(rv)
