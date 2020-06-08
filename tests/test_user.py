# test_user.py --- 
# 
# Filename: test_user.py
# Author: Louise <louise>
# Created: Fri May 15 21:41:06 2020 (+0200)
# Last-Updated: Mon Jun  8 16:22:14 2020 (+0200)
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

    def test_edit_post(self):
        """
        Tests that we can modify the user.
        """
        name = self.faker.name()
        email = self.faker.email()
        location = "Amsterdam, Netherlands"
        gender = "Woman"
        
        self.login(self.user.username, self.password)
        rv = self.client.post('/user/edit', data={
            "name": name,
            "email": email,
            "location": location,
            "gender": gender
        })

        self.assertRedirects(rv, f'/user/{self.user.username}')
        self.assertEqual(self.user.name, name)
        self.assertEqual(self.user.email, email)
        self.assertEqual(self.user.location, location)
        self.assertEqual(self.user.gender, gender)
        self.assertEqual(self.user.bio, "")
