# test_ajax.py ---
#
# Filename: test_ajax.py
# Author: Louise <louise>
# Created: Sun Jul  5 18:01:51 2020 (+0200)
# Last-Updated: Sun Jul  5 18:15:33 2020 (+0200)
#           By: Louise <louise>
#
from helpers import EditoggiaTestCase

from editoggia.models import Tag


class TestAjax(EditoggiaTestCase):
    """
    Tests views defined in the ajax blueprint.
    """

    def test_autocomplete_bad_model(self, client):
        """
        Test that without a correct model name we get
        a 400 error code.
        """
        rv = client.get("/ajax/autocomplete/BadModelName")
        assert rv.status_code == 400

    def test_autocomplete_fandom(self, client):
        """
        Test that the autocomplete empty returns
        the fandoms.
        """
        rv = client.get("/ajax/autocomplete/Fandom")

        assert rv.status_code == 200
        assert rv.json == dict(
            results=[{"id": "Original Work", "text": "Original Work"}]
        )

    def test_autocomplete_fandom_filter(self, client):
        """
        Test that the autocomplete returns only
        tags beginning with the query.
        """
        rv = client.get("/ajax/autocomplete/Fandom?q=L")

        assert rv.status_code == 200
        assert rv.json == dict(results=[])

    def test_autocomplete_tag(self, client):
        """
        Test that the autocomplete empty returns
        the tags.
        """
        Tag.create(name="Tagtest")
        rv = client.get("/ajax/autocomplete/Tag")

        assert rv.status_code == 200
        assert rv.json == dict(results=[{"id": "Tagtest", "text": "Tagtest"}])
