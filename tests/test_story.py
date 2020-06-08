# test_story.py --- 
# 
# Filename: test_story.py
# Author: Louise <louise>
# Created: Mon Jun  8 16:06:35 2020 (+0200)
# Last-Updated: Mon Jun  8 16:44:13 2020 (+0200)
#           By: Louise <louise>
# 
"""
These tests test the story blueprint.
"""
from faker import Faker

from editoggia.database import db
from editoggia.models import Story, Chapter

from helpers import EditoggiaTestCase

class TestStory(EditoggiaTestCase):
    """
    Test story views.
    """
    def test_index(self):
        """
        Tests the index.
        """
        story = self.create_stories(1)[0]
        rv = self.client.get('/story/')

        self.assert200(rv)
        self.assertIn(story.title.encode(), rv.data)

    def test_show_story(self):
        """
        Tests that a one-shot will produce a single page,
        without redirects.
        """
        story = self.create_stories(1)[0]
        rv = self.client.get(f'/story/{story.id}')

        # If we have a 200 code, that means no redirects
        # have occured.
        self.assert200(rv)
        self.assertIn(story.title.encode(), rv.data)

    def test_show_story_redirect(self):
        """
        Tests that a story with multiple chapters will
        redirect.
        """
        story = self.create_stories(1, 2)[0]
        rv = self.client.get(f'/story/{story.id}')

        self.assertRedirects(rv, f'/story/{story.id}/chapter/{story.chapters[0].id}')

    def test_show_chapter(self):
        """
        Tests that we can just show a chapter.
        """
        story = self.create_stories(1, 2)[0]
        rv = self.client.get(f'/story/{story.id}/chapter/{story.chapters[0].id}')

        self.assert200(rv)
        self.assertIn(story.chapters[0].title.encode(), rv.data)

    def test_story_index(self):
        """
        Tests that we can see the index of a particular story.
        """
        story = self.create_stories(1, 2)[0]
        rv = self.client.get(f'/story/{story.id}/index')

        self.assert200(rv)
        self.assertIn(story.chapters[0].title.encode(), rv.data)
        self.assertIn(story.chapters[1].title.encode(), rv.data)
