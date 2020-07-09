# bleach.py ---
#
# Filename: bleach.py
# Author: Louise <louise>
# Created: Tue Jul  7 21:14:43 2020 (+0200)
# Last-Updated: Wed Jul  8 23:43:41 2020 (+0200)
#           By: Louise <louise>
#
import re
from bleach.sanitizer import Cleaner
from bs4 import BeautifulSoup

class Bleacher():
    """
    The object intended to clean user input in summary
    and content. Produces safe HTML as a text (see concepts below.)

    Some concepts:
      - A text is a sequence of blocks.
      - A block is either a paragraph, a list or independant tags (hr).
      - A paragraph is some characters with inline tags, enclosed
        by a block-level tag.
      - A block-level tag is either blockquote, code, or p.
      - A list is a list tag (ol or ul) enclosing list items (li),
        enclosing itself some characters with inline tags.
      - An inline tag is either a, abbr, b, em, i, or strong.

    Some rules:
      - We construct a paragraph as either some text separated from
        the rest by two newlines, or as the very definition of a paragraph
        (some block-level tag enclosing text)
      - 
    """
    ALLOWED_TAGS = [
        "a", "abbr", "b", "br", "blockquote", "code",
        "em", "hr", "i", "li", "ol", "p", "strong", "ul"
    ]
    
    BLOCK_LEVEL_TAGS = [
        "ol", "ul", "blockquote", "code", "p"
    ]

    INDEPENDANT_TAG = [
        "hr"
    ]
    
    NEWLINES_RE = re.compile(r'\n+\s*\n+')
    SPACES_RE = re.compile(r'[ ]+')

    def __init__(self):
        """
        Creates the object.
        """
        self.cleaner = Cleaner(
            tags=self.ALLOWED_TAGS
        )

    def process_element(self, element):
        """
        Process each root element in the tree created by BeautifulSoup.
        """
        print(element)
        print("lol")
        
    def clean(self, text):
        """
        Actual function to clean. For now it uses the bleacher
        Cleaner, and collapses spaces and newlines.
        """
        cleaned_text = self.cleaner.clean(text)
        soup = BeautifulSoup(cleaned_text, features="lxml")
        text_body = soup.find('body')

        if text_body is None:
            return cleaned_text
        
        # Process each element, which are either
        for element in text_body.children:
            print(element)

        return str(soup)
