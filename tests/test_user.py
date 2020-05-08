# test_user.py --- 
# 
# Filename: test_user.py
# Author: Louise <louise>
# Created: Fri May  8 20:30:10 2020 (+0200)
# Last-Updated: Sat May  9 00:55:26 2020 (+0200)
#           By: Louise <louise>
# 
from app import create_app
from app.database import db
from app.users.models import User

from faker import Faker
import unittest

fake = Faker()

class TestUser(unittest.TestCase):
    def setUp(self):
        app = create_app("testing")
        db.app = app
        db.create_all()
        self.app = app.test_client()

    def test_signup_normal(self):
        password = fake.password()
        
        rv = self.app.post("/signup", data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": password,
            "confirm": password,
        }, follow_redirects=True)

        assert rv._status_code == 200
        assert b"Signed-up user" in rv.data
