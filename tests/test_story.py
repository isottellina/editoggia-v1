# test_story.py ---
#
# Filename: test_story.py
# Author: Louise <louise>
# Created: Mon Jun  8 16:06:35 2020 (+0200)
# Last-Updated: Tue Jul  7 16:54:10 2020 (+0200)
#           By: Louise <louise>
#
"""
These tests test the story blueprint.
"""
import pytest
from helpers import EditoggiaTestCase

from editoggia.database import db
from editoggia.models import Story


class TestStory(EditoggiaTestCase):
    """
    Test story views.
    """

    #
    # Views that are defined in view.py
    #

    def test_index(self, client, create_story):
        """
        Tests the index.
        """
        story = create_story()
        rv = client.get("/story/")

        assert rv.status_code == 200
        assert story.title.encode() in rv.data

    def test_show_story(self, client, create_story):
        """
        Tests that a one-shot will produce a single page,
        without redirects.
        """
        story = create_story()
        rv = client.get(f"/story/{story.id}")

        # If we have a 200 code, that means no redirects
        # have occured.
        assert rv.status_code == 200
        assert story.title.encode() in rv.data
        assert story.stats.hits == 1

    def test_show_story_as_author(self, app, create_user, create_story):
        """
        Same, but shouldn't add a hit.
        """
        user, _ = create_user()
        story = create_story(author=user)

        with app.test_client(user=user) as client:
            rv = client.get(f"/story/{story.id}")

        assert rv.status_code == 200
        assert story.title.encode() in rv.data
        assert story.stats.hits == 0

    def test_show_story_inexistent(self, client):
        """
        Should return 404.
        """
        rv = client.get("/story/2")
        assert rv.status_code == 404

    def test_show_story_redirect(self, client, create_story):
        """
        Tests that a story with multiple chapters will
        redirect.
        """
        story = create_story(nb_chapters=2)

        rv = client.get(f"/story/{story.id}", follow_redirects=True)
        assert len(rv.history) == 1  # Redirected once
        assert rv.request.path == f"/story/{story.id}/chapter/{story.chapters[0].id}"

    def test_show_story_redirect_restore(self, app, create_user, create_story):
        """
        Tests that a story with multiple chapters will
        redirect, to the last chapter read.
        """
        user, _ = create_user()
        story = create_story(nb_chapters=2)
        self.hit(user, story, chapter_nb=2)

        with app.test_client(user=user) as client:
            rv = client.get(f"/story/{story.id}", follow_redirects=True)

        assert len(rv.history) == 1
        assert rv.request.path == f"/story/{story.id}/chapter/{story.chapters[1].id}"

    def test_show_chapter(self, client, create_story):
        """
        Tests that we can just show a chapter, without history.
        """
        story = create_story(nb_chapters=2)
        rv = client.get(f"/story/{story.id}/chapter/{story.chapters[0].id}")

        assert rv.status_code == 200
        assert story.chapters[0].title.encode() in rv.data

    def test_story_index(self, client, create_story):
        """
        Tests that we can see the index of a particular story.
        """
        story = create_story(nb_chapters=2)
        rv = client.get(f"/story/{story.id}/index")

        assert rv.status_code == 200
        assert story.chapters[0].title.encode() in rv.data
        assert story.chapters[1].title.encode() in rv.data

    #
    # Views that are defined in post.py
    #

    def test_post_story_get(self, app, create_user):
        """
        Tests the GET route for post_story
        """
        user, _ = create_user()

        with app.test_client(user=user) as client:
            rv = client.get("/story/post")

        assert rv.status_code == 200

    def test_post_story_post(self, app, create_user):
        """
        Tests a POST request. If we get a 302 response,
        it means we were redirected and thus the view
        processed correctly.
        """
        user, _ = create_user()

        with app.test_client(user=user) as client:
            client.post(
                "/story/post",
                data={
                    "title": "Story test",
                    "summary": "Summary test",
                    "fandom": "Original Work,Fandom1",
                    "tags": "Tag1",
                    "total_chapters": "6",
                    "content": "Content test.",
                },
            )

        story = db.session.query(Story).filter(Story.title == "Story test").first()
        assert story
        assert story.author_id == user.id
        assert story.total_chapters == 6

    def test_post_story_post_unknown(self, app, create_user):
        """
        Tests an unknown total_chapters value.
        """
        user, _ = create_user()

        with app.test_client(user=user) as client:
            client.post(
                "/story/post",
                data={
                    "title": "Story test",
                    "summary": "Summary test",
                    "fandom": "Original Work",
                    "tags": "",
                    "total_chapters": "?",
                    "content": "Content test.",
                },
            )

        story = db.session.query(Story).filter(Story.title == "Story test").first()
        assert story
        assert story.total_chapters is None

    def test_post_story_post_bad_total(self, app, create_user):
        """
        Tests a bad total_chapters value.
        If we get a 200 code, it means we haven't had a redirect,
        which indicates that the form has only been reshown to us.
        """
        user, _ = create_user()

        with app.test_client(user=user) as client:
            rv = client.post(
                "/story/post",
                data={
                    "title": "Story test",
                    "summary": "Summary test",
                    "fandom": "Original Work",
                    "tags": "",
                    "total_chapters": "bad_value",
                    "content": "Content test.",
                },
            )

        assert rv.status_code == 200
        story = db.session.query(Story).filter(Story.title == "Story test").first()
        assert not story

    def test_post_chapter_post(self, app, create_user, create_story):
        """
        Tries to add a chapter.
        """
        user, _ = create_user()
        story = create_story(author=user, nb_chapters=1)

        with app.test_client(user=user) as client:
            client.post(
                f"/story/post/{story.id}/chapter",
                data={
                    "title": "Second chapter",
                    "nb": 2,
                    "content": "This is the content of the second chapter",
                },
            )

        assert len(story.chapters) == 2
        assert story.chapters[1].title == "Second chapter"

    def test_post_chapter_conflicting(self, app, create_user, create_story):
        """
        Tries to add a chapter with an already existing number.
        """
        user, _ = create_user()
        story = create_story(author=user)

        with app.test_client(user=user) as client:
            client.post(
                f"/story/post/{story.id}/chapter",
                data={
                    "title": "Second chapter",
                    "nb": 1,
                    "content": "This is the content of the second chapter",
                },
            )

        assert len(story.chapters) == 1

    #
    # Views that are defined in edit.py
    #
    def test_edit_story_bad_user(self, app, create_user, create_story):
        """
        Tests the edit_story view with a user
        that is not the user who wrote the story.
        """
        story = create_story()
        user, _ = create_user()

        with app.test_client(user=user) as client:
            rv = client.get(f"/story/edit/{story.id}")

        assert rv.status_code == 403

    def test_edit_story_get(self, app, create_user, create_story):
        """
        Tests the GET route for edit_story
        """
        user, _ = create_user()
        story = create_story(author=user)

        with app.test_client(user=user) as client:
            rv = client.get(f"/story/edit/{story.id}")

        assert rv.status_code == 200

    def test_edit_story_get_unknown_chapters(self, app, create_user, create_story):
        """
        Tests that a story with None as total_chapters get a '?' in the field.
        """
        user, _ = create_user()
        story = create_story(author=user)
        story.total_chapters = None

        with app.test_client(user=user) as client:
            rv = client.get(f"/story/edit/{story.id}")

        assert rv.status_code == 200
        assert b'value="?"' in rv.data

    def test_edit_story_post(self, app, create_user, create_story):
        """
        Tests the normal POST route for edit_story
        """
        user, _ = create_user()
        story = create_story(author=user)

        with app.test_client(user=user) as client:
            client.post(
                f"/story/edit/{story.id}",
                data={
                    "title": "New title",
                    "rating": story.rating,
                    "summary": story.summary,
                    "total_chapters": story.total_chapters,
                    "fandom": ["Original Work"],
                    "tag": ["Tag 1"],
                },
            )

        assert story.title == "New title"

    def test_edit_chapter_bad_user(self, app, create_user, create_story):
        """
        Tests the edit_chapter view with a user
        that is not the user who wrote the story.
        """
        user, _ = create_user()
        story = create_story()

        with app.test_client(user=user) as client:
            rv = client.get(f"/story/edit/{story.id}/chapter/{story.chapters[0].id}")

        rv.status_code == 403

    @pytest.mark.parametrize(
        "chapter_nb,should_work",
        (
            (1, True),  # Keep the same chapter number
            (3, True),  # New chapter number
            (2, False),  # New (conflicting) chapter number
        ),
    )
    def test_edit_chapter_post(
        self, app, create_user, create_story, chapter_nb, should_work
    ):
        """
        Tests a normal POST request for the edit_chapter.
        Should work if chapter_nb doesn't exist.
        """
        user, _ = create_user()
        story = create_story(author=user, nb_chapters=2)
        chapter = story.chapters[0]

        with app.test_client(user=user) as client:
            client.post(
                f"/story/edit/{story.id}/chapter/{chapter.id}",
                data={
                    "title": "New title",
                    "nb": chapter_nb,
                    "summary": chapter.summary,
                    "content": chapter.content,
                },
            )

        if should_work:
            assert chapter.title == "New title"
        else:
            assert chapter.title != "New title"

    #
    # Views defined in interaction.py
    #
    def test_like(self, app, create_user, create_story):
        """
        Like a story.
        """
        user, _ = create_user()
        story = create_story()

        with app.test_client(user=user) as client:
            rv = client.post(f"/story/{story.id}/like")

        assert rv.status_code == 200
        assert story in user.likes

    def test_unlike(self, app, create_user, create_story):
        """
        Unlike a story.
        """
        user, _ = create_user()
        story = create_story()

        user.likes.append(story)

        with app.test_client(user=user) as client:
            rv = client.post(f"/story/{story.id}/like")

        assert rv.status_code == 200
        assert story not in user.likes

    def test_comment(self, app, create_user, create_story):
        """
        Comment a chapter.
        """
        user, _ = create_user()
        story = create_story()

        user.likes.append(story)

        with app.test_client(user=user) as client:
            client.post(
                f"/story/{story.id}/chapter/{story.chapters[0].id}/comment",
                data={"comment": "Test comment"},
            )

        assert len(story.chapters[0].comments) == 1
