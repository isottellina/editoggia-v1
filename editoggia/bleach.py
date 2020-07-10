# bleach.py ---
#
# Filename: bleach.py
# Author: Louise <louise>
# Created: Tue Jul  7 21:14:43 2020 (+0200)
# Last-Updated: Fri Jul 10 02:22:46 2020 (+0200)
#           By: Louise <louise>
#
import re
from bleach.sanitizer import Cleaner
from bs4 import BeautifulSoup, NavigableString

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
    # Only tags that should be conserved.
    ALLOWED_TAGS = [
        "a", "abbr", "b", "br", "blockquote", "code",
        "em", "hr", "i", "li", "ol", "p", "strong", "ul"
    ]

    # Block-level tags. If something is outside this it will be put
    # in a <p> tag.
    BLOCK_LEVEL_TAGS = [
        "ol", "ul", "blockquote", "code", "p"
    ]

    # Tags that are independant and can happen outside a block-level.
    INDEPENDANT_TAGS = [
        "hr"
    ]

    # Tags that should just be ignored and only their content treated.
    IGNORE_TAGS = [
        "[document]", "html", "body"
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

    def open_tag(self, element, out_html=""):
        """
        Adds an open tag to the out_html string,
        with tag and attributes of the element given.
        Returns the string
        """
        return out_html + "<{tag}{attrs}>".format(
            tag=element.name,
            attrs="".join([
                f' {attr}="{element.attrs[attr]}"' for attr in element.attrs
            ])
        )

    def close_tag(self, element, out_html=""):
        """
        Adds a closing tag to the out_html string.
        Returns the string.
        """
        return out_html + f'</{element.name}>'
        
    def traverse_node(self, element, out_html=""):
        """
        Traverse every node in the HTML, and
        produces a new HTML string. We work on
        a string since the resulting HTML might
        have a completely different structure.
        """
        # Treatment if it's a string.
        if type(element) == NavigableString:
            return out_html + element.string
        
        # This is the treatment if this is a normal tag.
        # We recreate the opening tag if we're not supposed to
        # ignore it
        if element.name not in self.IGNORE_TAGS:
            out_html = self.open_tag(element, out_html)

        for child in element.children:
            out_html = self.traverse_node(child, out_html)
            
        # Now we close the tag
        if element.name not in self.IGNORE_TAGS:
            out_html = self.close_tag(element, out_html)

        return out_html

    def clean(self, text):
        """
        Actual function to clean. For now it uses the bleacher
        Cleaner, and collapses spaces and newlines.
        """
        cleaned_text = self.cleaner.clean(text)
        soup = BeautifulSoup(cleaned_text, features="lxml")

        # Treat HTML to create a new document
        new_doc = self.traverse_node(soup)
        print(new_doc)

        return cleaned_text
