# test_ajax.py --- 
# 
# Filename: test_ajax.py
# Author: Louise <louise>
# Created: Sun Jul  5 18:01:51 2020 (+0200)
# Last-Updated: Sun Jul  5 18:15:33 2020 (+0200)
#           By: Louise <louise>
# 
from helpers import EditoggiaTestCase

from editoggia.database import db
from editoggia.models import Tag

class TestAjax(EditoggiaTestCase):
    """
    Tests views defined in the ajax blueprint.
    """
    def test_autocomplete_bad_model(self):
        """
        Test that without a correct model name we get
        a 400 error code.
        """
        rv = self.client.get('/ajax/autocomplete/BadModelName')

        self.assert400(rv)

    def test_autocomplete_fandom(self):
        """
        Test that the autocomplete empty returns
        the fandoms.
        """
        rv = self.client.get('/ajax/autocomplete/Fandom')

        self.assert200(rv)
        self.assertEqual(rv.json, dict(
            results=[
                {"id": "Original Work", "text": "Original Work"}
            ]
        ))

    def test_autocomplete_fandom_filter(self):
        """
        Test that the autocomplete returns only
        tags beginning with the query.
        """
        rv = self.client.get('/ajax/autocomplete/Fandom?q=L')

        self.assert200(rv)
        self.assertEqual(rv.json, dict(
            results=[]
        ))
        
    def test_autocomplete_tag(self):
        """
        Test that the autocomplete empty returns
        the tags.
        """
        tag = Tag.create(name='Tagtest')
        rv = self.client.get('/ajax/autocomplete/Tag')

        self.assert200(rv)
        self.assertEqual(rv.json, dict(
            results=[
                {"id": "Tagtest", "text": "Tagtest"}
            ]
        ))
