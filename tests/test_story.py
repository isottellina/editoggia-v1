# test_story.py --- 
# 
# Filename: test_story.py
# Author: Louise <louise>
# Created: Mon Jun  8 16:06:35 2020 (+0200)
# Last-Updated: Sat Jun 27 14:02:11 2020 (+0200)
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

    #
    # Views that are defined in view.py
    #
    
    def test_index(self):
        """
        Tests the index.
        """
        story = self.create_story()
        rv = self.client.get('/story/')

        self.assert200(rv)
        self.assertIn(story.title.encode(), rv.data)

    def test_show_story(self):
        """
        Tests that a one-shot will produce a single page,
        without redirects.
        """
        story = self.create_story()
        rv = self.client.get(f'/story/{story.id}')

        # If we have a 200 code, that means no redirects
        # have occured.
        self.assert200(rv)
        self.assertIn(story.title.encode(), rv.data)
        self.assertEqual(story.stats.hits, 1)

    def test_show_story_as_author(self):
        """
        Same, but shouldn't add a hit.
        """
        story = self.create_story()
        self.login()
        
        rv = self.client.get(f'/story/{story.id}')

        self.assert200(rv)
        self.assertIn(story.title.encode(), rv.data)
        self.assertEqual(story.stats.hits, 0)

    def test_show_story_inexistent(self):
        """
        Should return 404.
        """
        rv = self.client.get(f'/story/2')

        self.assert404(rv)
        
    def test_show_story_redirect(self):
        """
        Tests that a story with multiple chapters will
        redirect.
        """
        story = self.create_story(2)
        rv = self.client.get(f'/story/{story.id}')

        self.assertRedirects(rv, f'/story/{story.id}/chapter/{story.chapters[0].id}')

    def test_show_chapter(self):
        """
        Tests that we can just show a chapter.
        """
        story = self.create_story(2)
        rv = self.client.get(f'/story/{story.id}/chapter/{story.chapters[0].id}')

        self.assert200(rv)
        self.assertIn(story.chapters[0].title.encode(), rv.data)

    def test_story_index(self):
        """
        Tests that we can see the index of a particular story.
        """
        story = self.create_story(2)
        rv = self.client.get(f'/story/{story.id}/index')

        self.assert200(rv)
        self.assertIn(story.chapters[0].title.encode(), rv.data)
        self.assertIn(story.chapters[1].title.encode(), rv.data)

    #
    # Views that are defined in post.py
    #
    
    def test_post_story_get(self):
        """
        Tests the GET route for post_story
        """
        self.login()
        rv = self.client.get('/story/post')

        self.assert200(rv)

    def test_post_story_post(self):
        """
        Tests a POST request. If we get a 302 response,
        it means we were redirected and thus the view
        processed correctly.
        """
        self.login()
        rv = self.client.post('/story/post', data={
            'title': 'Story test',
            'summary': 'Summary test',
            'fandom': 'Original Work,Fandom1',
            'tags': 'Tag1',
            'total_chapters': '6',
            'content': 'Content test.'
        })

        self.assertStatus(rv, 302)
        story = db.session.query(Story) \
                          .filter(Story.title == 'Story test') \
                          .first()
        self.assertNotEqual(story, None)
        self.assertEqual(story.total_chapters, 6)

    def test_post_story_post_unknown(self):
        """
        Tests an unknown total_chapters value.
        """
        self.login()
        rv = self.client.post('/story/post', data={
            'title': 'Story test',
            'summary': 'Summary test',
            'fandom': 'Original Work',
            'tags': '',
            'total_chapters': '?',
            'content': 'Content test.'
        })

        self.assertStatus(rv, 302)
        story = db.session.query(Story) \
                          .filter(Story.title == 'Story test') \
                          .first()
        self.assertNotEqual(story, None)
        self.assertEqual(story.total_chapters, None)

    def test_post_story_post_bad_total(self):
        """
        Tests a bad total_chapters value.
        If we get a 200 code, it means we haven't had a redirect,
        which indicates that the form has only been reshown to us.
        """
        self.login()
        rv = self.client.post('/story/post', data={
            'title': 'Story test',
            'summary': 'Summary test',
            'fandom': 'Original Work',
            'tags': '',
            'total_chapters': 'bad_value',
            'content': 'Content test.'
        })

        self.assert200(rv)
        story = db.session.query(Story) \
                          .filter(Story.title == 'Story test') \
                          .first()
        
        # story wasn't created
        self.assertEqual(story, None)
        
    def test_post_chapter_get(self):
        """
        Tests the GET route for post_chapter
        """
        self.login()
        story = self.create_story()

        rv = self.client.get(f'/story/post/{story.id}/chapter')

        self.assert200(rv)

    def test_post_chapter_post(self):
        """
        Tries to add a chapter.
        """
        self.login()
        story = self.create_story()
        
        rv = self.client.post(f'/story/post/{story.id}/chapter', data={
            'title': 'Second chapter',
            'nb': 2,
            'content': 'This is the content of the second chapter'
        })

        self.assertStatus(rv, 302)
        self.assertEqual(len(story.chapters), 2)
        self.assertEqual(story.chapters[1].title, 'Second chapter')

    def test_post_chapter_conflicting(self):
        """
        Tries to add a chapter with an already existing number.
        """
        self.login()
        story = self.create_story()
        
        rv = self.client.post(f'/story/post/{story.id}/chapter', data={
            'title': 'Second chapter',
            'nb': 1,
            'content': 'This is the content of the second chapter'
        })

        self.assert200(rv)
        self.assertEqual(len(story.chapters), 1)

    #
    # Views that are defined in edit.py
    #
    def test_edit_story_bad_user(self):
        """
        Tests the edit_story view with a user 
        that is not the user who wrote the story.
        """
        story = self.create_story()

        new_user, new_password = self.create_user()
        self.login(new_user.username, new_password)

        rv = self.client.get(f'/story/edit/{story.id}')
        self.assert403(rv)
        
    def test_edit_story_get(self):
        """
        Tests the GET route for edit_story
        """
        story = self.create_story()

        self.login()

        rv = self.client.get(f'/story/edit/{story.id}')
        self.assert200(rv)

    def test_edit_story_get_unknown_chapters(self):
        """
        Tests that a story with None as total_chapters get a '?' in the field.
        """
        story = self.create_story()
        story.total_chapters = None
        db.session.commit()

        self.login()

        rv = self.client.get(f'/story/edit/{story.id}')
        self.assert200(rv)
        self.assertIn(b'value="?"', rv.data)

    def test_edit_story_post(self):
        """
        Tests the normal POST route for edit_story
        """
        story = self.create_story()
        self.login()

        rv = self.client.post(f'/story/edit/{story.id}', data={
            'title': 'New title',
            'rating': story.rating,
            'summary': story.summary,
            'total_chapters': story.total_chapters,
            'fandom': ['Original Work'],
            'tag': ['Tag 1']
        })
        
        self.assertStatus(rv, 302)
        self.assertEqual(story.title, 'New title')

    def test_edit_chapter_bad_user(self):
        """
        Tests the edit_chapter view with a user 
        that is not the user who wrote the story.
        """
        story = self.create_story()
        chapter = story.chapters[0]

        new_user, new_password = self.create_user()
        self.login(new_user.username, new_password)

        rv = self.client.get(f'/story/edit/{story.id}/chapter/{chapter.id}')
        self.assert403(rv)
        
    def test_edit_chapter_get(self):
        """
        Tests the GET route for edit_chapter
        """
        story = self.create_story()
        chapter = story.chapters[0]

        self.login()

        rv = self.client.get(f'/story/edit/{story.id}/chapter/{chapter.id}')
        self.assert200(rv)

    def test_edit_chapter_post(self):
        """
        Tests a normal POST request for the edit_chapter.
        Should work with the same chapter nb.
        """
        story = self.create_story(2)
        chapter = story.chapters[0]

        self.login()

        rv = self.client.post(f'/story/edit/{story.id}/chapter/{chapter.id}', data={
            'title': 'New title',
            'nb': chapter.nb,
            'summary': chapter.summary,
            'content': chapter.content
        })
        
        self.assertStatus(rv, 302)

    def test_edit_chapter_post_change_nb(self):
        """
        Tests a normal POST request for the edit_chapter, but with a different
        chapter_nb. Should work.
        """
        story = self.create_story(2)
        chapter = story.chapters[0]

        self.login()

        rv = self.client.post(f'/story/edit/{story.id}/chapter/{chapter.id}', data={
            'title': 'New title',
            'nb': 3,
            'summary': chapter.summary,
            'content': chapter.content
        })
        
        self.assertStatus(rv, 302)
        self.assertEqual(chapter.nb, 3)

    def test_edit_chapter_post_change_nb_conflict(self):
        """
        Tests a normal POST request for the edit_chapter, but with a different
        chapter_nb, but this one is taken. Shouldn't work.
        """
        story = self.create_story(2)
        chapter = story.chapters[0]

        self.login()

        rv = self.client.post(f'/story/edit/{story.id}/chapter/{chapter.id}', data={
            'title': 'New title',
            'nb': 2,
            'summary': chapter.summary,
            'content': chapter.content
        })
        
        self.assert200(rv)
        self.assertNotEqual(chapter.nb, 2)
