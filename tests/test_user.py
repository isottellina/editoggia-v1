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

from editoggia.database import db
from editoggia.models import User

from helpers import EditoggiaTestCase

class TestUser(EditoggiaTestCase):
    """
    Test view profile.
    """
    def test_view_profile_doesnt_exist(self):
        """
        Tests that the app 404s when an user doesn't exist.
        """
        rv = self.client.get('/user/notexist')

        self.assert404(rv)

    def test_view_profile_normal(self):
        """
        Tests we can access a profile that exist.
        """
        # We put a little info in the profile
        self.user.location = "Paris, France"
        self.user.birthdate = datetime.date(1995, 5, 3)

        age = (datetime.date.today() - self.user.birthdate) // \
            datetime.timedelta(days=365.2425)
        
        # We get the URL to do the actual request
        url = f'/user/{self.user.username}'
        rv = self.client.get(url)

        self.assert200(rv)
        self.assertIn(b"Paris, France", rv.data)
        self.assertIn(str(age).encode(), rv.data)
        
    def test_view_profile_normal_wo_birthdate(self):
        """
        Tests we can access a profile that exist, without birthdate.
        """
        # We put a little info in the profile
        self.user.location = "Paris, France"
        
        # We get the URL to do the actual request
        url = f'/user/{self.user.username}'
        rv = self.client.get(url)

        self.assert200(rv)
        self.assertIn(b"Paris, France", rv.data)
        self.assertNotIn(b'id="age"', rv.data)
        
    def test_view_profile_likes(self):
        """
        Tests we can access a profile's likes.
        """
        story = self.create_story()
        self.like(story)
        
        # We get the URL to do the actual request
        url = f'/user/{self.user.username}/liked'
        rv = self.client.get(url)

        self.assert200(rv)
        self.assertIn(story.title.encode(), rv.data)

    def test_view_profile_history(self):
        """
        Tests we can access a profile's history.
        """
        story = self.create_story()
        self.hit(story)
        
        # We get the URL to do the actual request
        url = f'/user/{self.user.username}/history'
        rv = self.client.get(url)

        self.assert200(rv)
        self.assertIn(story.title.encode(), rv.data)

    """
    Test edit profile.
    """
    def test_edit_get(self):
        """
        Tests that we get the form when we send a
        GET request.
        """
        self.login(self.user.username, self.password)
        rv = self.client.get('/user/edit')

        self.assert200(rv)
        self.assertIn(b'<form', rv.data)
        self.assertIn(f'value="{self.user.name}"'.encode(), rv.data)

    def generic_test_edit_post(self, data={}):
        """
        Generic test for edit_post view.
        """
        base_data = {
            "name": self.faker.name(),
            "email": self.faker.email(),
            "location": "Amsterdam, Netherlands",
            "gender": "Woman",
            "language": self.app.config["ACCEPTED_LANGUAGES"][0]
        }
        base_data.update(data)
        
        self.login(self.user.username, self.password)
        rv = self.client.post('/user/edit', data=base_data)

        self.assertRedirects(rv, f'/user/{self.user.username}')
        self.assertEqual(self.user.name, base_data['name'])
        self.assertEqual(self.user.email, base_data['email'])
        self.assertEqual(self.user.location, base_data['location'])
        self.assertEqual(self.user.gender, base_data['gender'])
        self.assertEqual(self.user.bio, "")
        
    def test_edit_post(self):
        """
        Tests that we can modify the user.
        """
        self.generic_test_edit_post({
            "birthdate": "1970-01-01"
        })

    def test_edit_post_no_birthdate(self):
        """
        Tests that the birthdate can be empty.
        """
        self.generic_test_edit_post()

    def test_edit_post_no_birthdate(self):
        """
        Tests that a bad birthdate is not accepted
        """
        self.login(self.user.username, self.password)
        rv = self.client.post('/user/edit', data={
            "name": self.faker.name(),
            "email": self.faker.email(),
            "location": "Amsterdam, Netherlands",
            "gender": "Woman",
            "birthdate": "badone",
            "language": self.app.config["ACCEPTED_LANGUAGES"][0]
        })

        self.assert200(rv)
