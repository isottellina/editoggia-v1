# bleacher.py ---
#
# Filename: bleacher.py
# Author: Louise <louise>
# Created: Tue Jul  7 21:14:43 2020 (+0200)
# Last-Updated: Sat Jul 11 23:19:25 2020 (+0200)
#           By: Louise <louise>
#
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
"""
import re
from bleach.sanitizer import Cleaner
from bs4 import BeautifulSoup, NavigableString, Tag

# Only tags that should be conserved.
ALLOWED_TAGS = [
    "a",
    "abbr",
    "b",
    "br",
    "blockquote",
    "code",
    "em",
    "hr",
    "i",
    "li",
    "ol",
    "p",
    "strong",
    "ul",
]


def bleach(text):
    """
    Actual function to clean.
    """
    cleaner = Cleaner(tags=ALLOWED_TAGS)

    cleaned_text = cleaner.clean(text)
    soup = BeautifulSoup(cleaned_text, features="html.parser")

    # Treat HTML to create a new document
    new_doc = HTMLProducer()
    new_doc.traverse_node(soup)

    return str(new_doc)


class HTMLProducer:
    """
    The object that produces HTML, used by the Bleacher.
    It uses internal state, so it's a separate object.

    I should get a medal for this my brain melted quite a few times.
    """

    # Block-level tags. If something is outside this it will be put
    # in a <p> tag.
    BLOCK_LEVEL_TAGS = ["ol", "ul", "blockquote", "code", "p", "hr"]

    # Tags that are independant and can happen outside a block-level.
    INDEPENDANT_TAGS = ["hr"]

    # Tags that should just be ignored and only their content treated.
    # They're top level tags.
    IGNORE_TAGS = ["[document]", "html", "body"]

    # Tags that should be conserved as-is
    CONSERVE_TAGS = [
        "a",
        "abbr",
        "acronym",
        "address",
        "br",
        "dl",
        "hr",
        "ol",
        "p",
        "pre",
        "blockquote",
        "ul",
    ]

    # Tags we don't want breaks before or after
    NO_BREAK_TAGS = ["blockquote", "br", "dl", "hr", "ol", "p", "pre", "code", "ul"]

    BS4_FORMATTER = "minimal"

    SINGLE_NEWLINE_RE = re.compile(r"\n")
    MULTIPLE_NEWLINES_RE = re.compile(r"\n+\s*\n+")
    TAGS_TOGETHER_RE = re.compile(r"><")

    def __init__(self):
        # The stack of tags
        self.stack = []

        # String to produce.
        self.out_html = ""

    def open_tag(self, element):
        """
        Adds an open tag to the out_html string,
        with tag and attributes of the element given.
        Returns the string
        """
        self.out_html += "<{tag}{attrs}>".format(
            tag=element.name,
            attrs="".join(
                [f' {attr}="{element.attrs[attr]}"' for attr in element.attrs]
            ),
        )

    def close_tag(self, tag_name):
        """
        Adds a closing tag to the out_html string.
        Returns the string.
        """
        self.out_html += f"</{tag_name}>"

    def open_p(self):
        """
        Create a paragraph.
        """
        self.stack.append("p")
        self.out_html += "<p>"

    def open_p_str(self):
        """
        Same as open_p, but returns a string.
        """
        self.stack.append("p")
        return "<p>"

    def close_block(self):
        """
        If we are creating a paragraph, close it.
        """
        for item in reversed(self.stack):
            self.stack.pop()
            self.close_tag(item)

            if item in self.BLOCK_LEVEL_TAGS:
                return

    def close_until(self, tag_name):
        """
        Close until we encounter this element name
        in the stack.
        """
        for item in reversed(self.stack):
            self.stack.pop()
            self.close_tag(item)

            if item == tag_name:
                return

    def close_block_str(self):
        """
        Closes a block, not in internal, but in
        another string.
        """
        out = ""
        for item in reversed(self.stack):
            self.stack.pop()
            out += f"</{item}>"

            if item in self.BLOCK_LEVEL_TAGS:
                return out

    def in_block(self):
        """
        Are we currently in a block?
        """
        for tag in self.stack:
            if tag in self.BLOCK_LEVEL_TAGS:
                return True
        return False

    def add_string(self, string):
        """
        Adds a string to the HTML.
        """
        self.out_html += string

    def traverse_node(self, element):
        """
        Traverse every node in the HTML, and
        produces a new HTML string. We work on
        a string since the resulting HTML might
        have a completely different structure.
        """
        # Some tags we just keep as-is.
        if type(element) == Tag and element.name in self.CONSERVE_TAGS:
            if element.name in self.BLOCK_LEVEL_TAGS and self.in_block():
                self.close_block()
                self.add_string(str(element))
            elif element.name not in self.BLOCK_LEVEL_TAGS and not self.in_block():
                self.add_string(
                    "<p>" + element.decode(formatter=self.BS4_FORMATTER) + "</p>"
                )
            else:
                self.add_string(element.decode(formatter=self.BS4_FORMATTER))

            return

        # If it's a string just add it (and open a paragraph if we need to)
        if type(element) == NavigableString:
            text = element.output_ready(formatter=self.BS4_FORMATTER)

            # If the previous tag is a NO_BREAK_TAG, strip
            if (
                element.previous_sibling
                and element.previous_sibling.name in self.NO_BREAK_TAGS
            ):
                text = text.lstrip()
            # If the next tag is a NO_BREAK_TAG, strip
            if element.next_sibling and element.next_sibling.name in self.NO_BREAK_TAGS:
                text = text.rstrip()

            # We only open a paragraph for strings not empty
            if not self.in_block() and text != "":
                self.open_p()

            # For several newlines, we begin a new paragraph
            text = self.MULTIPLE_NEWLINES_RE.sub(
                lambda _: self.close_block_str() + self.open_p_str(), text
            )

            # We replace a newline with a break tag.
            text = self.SINGLE_NEWLINE_RE.sub("<br/>\n", text)

            # After these substitutions, we insert newlines between the tags.
            text = self.TAGS_TOGETHER_RE.sub(">\n<", text)

            self.add_string(text)
            return

        # Some tags we descend into. This now must be a tag.
        if element.name not in self.IGNORE_TAGS:
            # If it's an inline tag and we're not in a block, create a tag.
            if element.name not in self.BLOCK_LEVEL_TAGS and not self.in_block():
                self.open_p()
            self.open_tag(element)
            self.stack.append(element.name)

        for child in element.children:
            self.traverse_node(child)

        self.close_until(element.name)

    def __str__(self):
        return self.out_html
