# helpers.py --- 
# 
# Filename: helpers.py
# Author: Louise <louise>
# Created: Fri May 15 21:42:56 2020 (+0200)
# Last-Updated: Sun Jun 21 21:27:47 2020 (+0200)
#           By: Louise <louise>
# 
from flask_testing import TestCase
from faker import Faker

from editoggia import create_app
from editoggia.database import db
from editoggia.models import Fandom, FandomCategory, Story, Chapter, User

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
            password=self.password
        )

        # Create a fandom and fandomcategory
        self.category = FandomCategory.create(name="Other")
        self.fandom = Fandom.create(name="Original Work",
                                    category=self.category,
                                    waiting_mod=False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        """
        Helper function to login as an user.
        """
        return self.client.post('/login', data={
            "username": username,
            "password": password
        }, follow_redirects=True)

    def create_stories(self, nb_stories, nb_chapters=1,
                       author=None, fandom=None):
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
                commit=False
            )

            for i in range(nb_chapters):
                chapter = Chapter.create(
                    title=self.faker.sentence(),
                    nb=i+1,
                    summary=" ".join(self.faker.sentences(nb=5)),
                    content=self.faker.text(max_nb_chars=3000),
                    story=story,
                    commit=False
                )

            stories.append(story)

        db.session.commit()
        return stories
