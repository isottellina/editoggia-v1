# helpers.py ---
#
# Filename: helpers.py
# Author: Louise <louise>
# Created: Fri May 15 21:42:56 2020 (+0200)
# Last-Updated: Sat Jul 11 23:34:06 2020 (+0200)
#           By: Louise <louise>
#
from flask_testing import TestCase
from faker import Faker
import pytest

from editoggia import create_app
from editoggia.database import db
from editoggia.models import Fandom, FandomCategory, Story, Chapter, User
from editoggia.models import Role, Permission


@pytest.mark.usefixtures("transaction")
class EditoggiaTestCase(TestCase):
    def create_app(self):
        return create_app("testing")

    def setUp(self):
        # Create all tables
        db.create_all()

        # Create a faker to help with tests
        self.faker = Faker()

        # Register a user to test
        self.password = self.faker.password()

        self.user = User.create(
            username=self.faker.user_name(),
            name=self.faker.name(),
            email=self.faker.email(),
            password=self.password,
        )

        # Create a fandom and fandomcategory
        self.category = FandomCategory.create(name="Other")
        self.fandom = Fandom.create(
            name="Original Work", category=self.category, waiting_mod=False
        )

        # Create permissions and roles
        admin_perm = Permission.create(
            name="admin.ACCESS_ADMIN_INTERFACE",
            description="Can access the admin interface.",
        )
        moderation_perm = Permission.create(
            name="mod.ACCESS_TAG_INTERFACE",
            description="Can access the interface to manage tag and fandoms.",
        )

        admin_role = Role.create(
            name="Administrator",
            description="Administrator of the website.",
            permissions=[admin_perm, moderation_perm],
        )

        # Assign role to the user
        self.user.roles = [admin_role]

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username=None, password=None):
        """
        Helper function to login as an user.
        If called without an argument, will login
        using parameters created during init.
        """
        username = username if username is not None else self.user.username
        password = password if password is not None else self.password

        return self.client.post(
            "/login",
            data={"username": username, "password": password},
            follow_redirects=True,
        )

    def create_user(self, username=None):
        """
        Creates a user and returns (user, password).
        """
        username = username if username is not None else self.faker.user_name()
        password = self.faker.password()

        user = User.create(
            username=username,
            name=self.faker.name(),
            email=self.faker.email(),
            password=password,
        )

        return user, password

    def create_story(self, nb_chapters=1, author=None, fandom=None):
        return self.create_stories(1, nb_chapters, author, fandom)[0]

    def create_stories(self, nb_stories, nb_chapters=1, author=None, fandom=None):
        """
        Create nb_stories stories with nb_chapters chapters each,
        written by author (self.user if None).
        """
        author = author if author else self.user
        fandom = fandom if fandom else self.fandom
        stories = []

        for _ in range(nb_stories):
            story = Story.create(
                title=self.faker.sentence(),
                summary=" ".join(self.faker.sentences(nb=5)),
                total_chapters=nb_chapters,
                author=author,
                fandom=[fandom],
                commit=False,
            )

            for i in range(nb_chapters):
                chapter = Chapter.create(
                    title=self.faker.sentence(),
                    nb=i + 1,
                    summary=" ".join(self.faker.sentences(nb=5)),
                    content=self.faker.text(max_nb_chars=3000),
                    story=story,
                    commit=False,
                )

            stories.append(story)

        db.session.commit()
        return stories

    def hit(self, story, chapter_nb=1, user=None):
        """
        Add a hit of the story to user.
        """
        user = user if user is not None else self.user
        user.add_to_history(story, chapter_nb)

    def like(self, story, user=None):
        """
        Add story to stories liked by user user.
        """
        user = user if user is not None else self.user
        user.likes.append(story)
