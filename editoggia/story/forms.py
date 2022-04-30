# forms.py ---
#
# Filename: forms.py
# Author: Louise <louise>
# Created: Fri May 22 18:40:58 2020 (+0200)
# Last-Updated: Thu Jul  9 14:42:49 2020 (+0200)
#           By: Louise <louise>
#
from flask_babelex import gettext
from flask_wtf import FlaskForm
from wtforms.fields import IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError

from editoggia.forms.fields import Select2Field, Select2MultipleAutocompleteField

#
# Story and chapter forms.
#


class StoryForm(FlaskForm):
    title = StringField(
        gettext("Title"),
        validators=[
            DataRequired(message=gettext("Title can't be empty.")),
            Length(max=255, message=gettext("Title must be less than 255 characters.")),
        ],
    )

    rating = Select2Field(
        gettext("Rating"),
        choices=[
            (None, gettext("Not rated")),
            ("General audiences", gettext("General audiences")),
            ("Teen and up audiences", gettext("Teen and up audiences")),
            ("Mature", gettext("Mature")),
            ("Explicit", gettext("Explicit")),
        ],
        # We have to coerce the value to get the None value right
        coerce=lambda x: None if x == "None" else x,
    )

    summary = TextAreaField(
        gettext("Summary"),
        default="",
        validators=[
            Length(
                max=1000, message=gettext("Summary must be less than 1000 characters.")
            )
        ],
    )

    total_chapters = StringField(gettext("Total chapters"), default="1")

    # This is the name of the chapter that will be posted,
    # if the story has multiple ones.
    chapter_title = StringField(
        gettext("Chapter title"),
        validators=[
            Length(max=255, message=gettext("Title must be less than 255 characters."))
        ],
    )

    fandom = Select2MultipleAutocompleteField(gettext("Fandoms"), model_name="Fandom")
    tags = Select2MultipleAutocompleteField(gettext("Tags"), model_name="Tag")

    def __init__(self, *args, **kwargs):
        """
        Overload init so we can modify the obj parameter,
        so that if total_chapters == None, we can modify it to '?'.
        Using default parameter in the field is not enough.
        """
        FlaskForm.__init__(self, *args, **kwargs)
        if self.total_chapters.data is None:
            self.total_chapters.process_data("?")

    def validate_total_chapters(self, field):
        """
        Validate the total_chapters field.
        """
        if field.data.isdecimal():
            field.data = int(field.data)
        elif field.data == "?":
            field.data = None
        else:
            raise ValidationError(gettext("Total chapters must be '?' or a number."))

    def populate_select2(
        self, fandoms=[], tags=[]
    ):  # pylint: disable=dangerous-default-value
        """
        Populate the fandom and tags fields, so they can be used.
        We disable dangerous default value lint, since we don't
        modify the argument.
        """

        def populate_field(field, base):
            """
            Populate a field.
            """
            field.choices = [(base_sgl.name, base_sgl.name) for base_sgl in base]
            field.process_data([base_sgl.name for base_sgl in base])

        populate_field(self.fandom, fandoms)
        populate_field(self.tags, tags)


class PostStoryForm(StoryForm):
    """
    The form to post a story. It's got a content
    field, to create the first chapter.
    """

    content = TextAreaField(
        gettext(
            "Content",
            validators=[
                Length(
                    min=20, message=gettext("Content must be at least 20 characters.")
                )
            ],
        )
    )


class EditStoryForm(StoryForm):
    """
    This form is for story editing. It doesn't
    require any other field, for now. Might in
    the future.
    """


class ChapterForm(FlaskForm):
    """
    Form to post or edit a chapter.
    """

    title = StringField(
        gettext("Title"),
        validators=[
            Length(max=255, message=gettext("Title must be less than 255 characters."))
        ],
    )

    nb = IntegerField(
        gettext("Chapter number"),
        validators=[
            DataRequired(message=gettext("Chapter number can't be empty.")),
            NumberRange(
                min=0, message=gettext("Chapter number can't be less than zero.")
            ),
        ],
    )

    summary = TextAreaField(
        gettext("Summary"),
        default="",
        validators=[
            Length(
                max=1000, message=gettext("Summary must be less than 1000 characters.")
            )
        ],
    )

    content = TextAreaField(
        gettext(
            "Content",
            validators=[
                Length(
                    min=20, message=gettext("Content must be at least 20 characters.")
                )
            ],
        )
    )

    def __init__(self, *args, story=None, chapter=None, **kwargs):
        """
        Overload init to add a story parameter, to enable checking
        unique constraint for the chapter number in the form.
        If editing, we also pass the chapter object.
        """
        FlaskForm.__init__(self, *args, **kwargs)
        self.story = story
        self.chapter = chapter

    def validate_nb(self, field):
        """
        Validate the nb field. In practice, we check that the
        chapter number is not already taken by another chapter.
        """

        def is_same_number(other_chapter):
            """
            Returns true if the other_chapter has the same number
            as the chapter of the form, but a different ID (because
            if it has the same ID, it's the same chapter so it's
            allowed). If the chapter is None, returns True if the
            chapter has the same number.
            """
            if self.chapter:
                return (
                    field.data == other_chapter.nb
                    and self.chapter.id != other_chapter.id
                )
            return field.data == other_chapter.nb

        if any(map(is_same_number, self.story.chapters)):
            raise ValidationError(gettext("This chapter number already exists."))


#
# Interaction forms
#


class CommentForm(FlaskForm):
    """
    Form to post a comment on a chapter.
    """

    comment = TextAreaField(gettext("Comment"), validators=[DataRequired()])


class LikeForm(FlaskForm):
    """
    Form to like a story. There are no fields, but we should
    still check for CSRF.
    """
