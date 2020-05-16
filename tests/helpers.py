# helpers.py --- 
# 
# Filename: helpers.py
# Author: Louise <louise>
# Created: Fri May 15 21:42:56 2020 (+0200)
# Last-Updated: Sat May 16 21:40:59 2020 (+0200)
#           By: Louise <louise>
# 
from flask_testing import TestCase
from faker import Faker

from editoggia import create_app
from editoggia.database import db
from editoggia.user.models import User

class EditoggiaTestCase(TestCase):
    def create_app(self):
        return create_app("testing")
    
    def setUp(self):
        # Create all tables
        db.create_all()

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
