# tests_home.py ---
#
# Filename: tests_home.py
# Author: Louise <louise>
# Created: Fri May  8 19:53:02 2020 (+0200)
# Last-Updated: Sat May 16 17:57:02 2020 (+0200)
#           By: Louise <louise>
#
from helpers import EditoggiaTestCase

class TestHome(EditoggiaTestCase):
    def test_home(self):
        """
        Tests the home page returns 200 in the normal
        case.
        """
        rv = self.client.get("/")

        self.assert200(rv)
        self.assertEqual(
            rv.headers["Content-Type"],
            "text/html; charset=utf-8"
        )
