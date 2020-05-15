# helpers.py --- 
# 
# Filename: helpers.py
# Author: Louise <louise>
# Created: Fri May 15 21:42:56 2020 (+0200)
# Last-Updated: Fri May 15 21:48:06 2020 (+0200)
#           By: Louise <louise>
# 
import unittest
from faker import Faker

from app import create_app
from app.database import db
from app.user.models import User

class EditoggiaTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app("testing")
        db.app = app
        db.create_all()
        self.app = app.test_client()

        # Create a faker to help with tests
        self.faker = Faker()
        
        # Register a user to test
        self.password = self.faker.password()
        
        self.user = User.create(
            username=self.faker.user_name(),
            name=self.faker.name(),
            email=self.faker.email(),
            password=self.password
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()
