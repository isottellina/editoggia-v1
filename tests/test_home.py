# tests_home.py --- 
# 
# Filename: tests_home.py
# Author: Louise <louise>
# Created: Fri May  8 19:53:02 2020 (+0200)
# Last-Updated: Fri May  8 20:26:27 2020 (+0200)
#           By: Louise <louise>
# 
from editoggia import create_app
import unittest

class TestHome(unittest.TestCase):
    def test_home(self):
        """
        Tests the home page returns 200 in the normal
        case.
        """
        app = create_app("testing")

        with app.test_client() as client:
            rv = client.get("/")

            assert rv._status_code == 200
            assert rv.headers["Content-Type"] == "text/html; charset=utf-8"
