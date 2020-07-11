# test_bleach.py --- 
# 
# Filename: test_bleach.py
# Author: Louise <louise>
# Created: Sat Jul 11 02:09:09 2020 (+0200)
# Last-Updated: Sat Jul 11 04:03:21 2020 (+0200)
#           By: Louise <louise>
# 
"""
Tests for the bleach function.
Here we just use the normal TestCase.
"""
from unittest import TestCase

from editoggia.bleacher import bleach

class TestBleach(TestCase):
    def test_cant_have_forbidden_tags(self):
        """
        Tests that forbidden tags are bleached.
        """
        result = bleach('<div><img src="lol.png" /><div>')

        self.assertEqual(result, '<p>&lt;div&gt;&lt;img src="lol.png" /&gt;&lt;div&gt;</p>')
        
    def test_dont_modify_p_tag(self):
        """
        Tests that a p tag is not modified.
        """
        result = bleach("<p>Eh, that's a\n p tag!</p>")

        self.assertEqual(result, "<p>Eh, that's a\n p tag!</p>")

    def test_conserve_tag_outside_p(self):
        """
        Tests that a conserved tag outside of a block is put inside one.
        """
        result = bleach('<a href="#">That is a link!</a>')

        self.assertEqual(result, '<p><a href="#">That is a link!</a></p>')

    def test_create_p_tag_and_break(self):
        """
        Tests that outside of a block, it creates a block,
        and creates break for newlines.
        """
        result = bleach("Eh, that's outside\n of a p tag!")

        self.assertEqual(result, "<p>Eh, that's outside<br/>\n of a p tag!</p>")
        
    def test_create_p_tag_with_inline(self):
        """
        Same test but with inline tags.
        """
        result = bleach("<i>Eh</i>, that's outside\n of a p tag!")

        self.assertEqual(result, "<p><i>Eh</i>, that's outside<br/>\n of a p tag!</p>")
        
    def test_create_multiple_p_tags(self):
        """
        Created multiple paragraphs with multiple lines.
        """
        result = bleach("First paragraph\n\nSecond paragraph")

        self.assertEqual(result, "<p>First paragraph</p>\n<p>Second paragraph</p>")

    def test_no_break_before(self):
        """
        Tests the strip in the beginning of a string.
        """
        result = bleach("<p>First paragraph</p>\nSecond paragraph")

        self.assertEqual(result, "<p>First paragraph</p><p>Second paragraph</p>")
        
    def test_no_break_after(self):
        """
        Tests the strip after a string (also closing of paragraph tags)
        """
        result = bleach("First paragraph\n<p>Second paragraph</p>")

        self.assertEqual(result, "<p>First paragraph</p><p>Second paragraph</p>")
