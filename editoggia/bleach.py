# bleach.py ---
#
# Filename: bleach.py
# Author: Louise <louise>
# Created: Tue Jul  7 21:14:43 2020 (+0200)
# Last-Updated: Wed Jul  8 02:05:33 2020 (+0200)
#           By: Louise <louise>
#
import re
from bleach.sanitizer import Cleaner, ALLOWED_TAGS


class Bleacher():
    """
    A wrapper class of Cleaner to do slightly more stuff, like
    collapsing whitespace.
    """
    NEWLINES_RE = re.compile(r'\n+\s*\n+')
    SPACES_RE = re.compile(r'[ ]+')

    def __init__(self):
        """
        Creates the object.
        """
        self.cleaner = Cleaner(
            tags=ALLOWED_TAGS + ['p']
        )

    def clean(self, text):
        """
        Actual function to clean. For now it uses the bleacher
        Cleaner, and collapses spaces and newlines.
        """
        cleaned_text = self.cleaner.clean(text)
        cleaned_text = self.NEWLINES_RE.sub('\n', cleaned_text)
        cleaned_text = self.SPACES_RE.sub(' ', cleaned_text)

        return cleaned_text
