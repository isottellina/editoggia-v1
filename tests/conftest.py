from contextlib import contextmanager
from typing import Iterator

import alembic.command
import faker
import psycopg2
import pytest
from flask.app import Flask
from flask_login import FlaskLoginClient
from sqlalchemy import event

from editoggia import create_app
from editoggia.config import TestingConfig
from editoggia.database import db
from editoggia.models.fandom import Fandom
from editoggia.models.story import Chapter, Story
from editoggia.models.user import Role, User


@contextmanager
def postgres_cursor(db_name: str = "postgres"):
    """
    Cursor to a postgres database.
    """
    connection = psycopg2.connect(
        user=TestingConfig.POSTGRES_USER,
        password=TestingConfig.POSTGRES_PASSWORD,
        host=TestingConfig.POSTGRES_HOST,
        port=TestingConfig.POSTGRES_PORT,
        dbname=db_name,
    )
    connection.autocommit = True

    yield connection.cursor()


def database_exists(cursor, db_name: str) -> bool:
    """
    Whether a certain database exists.
    """
    cursor.execute(
        """
        SELECT datname
        FROM pg_catalog.pg_database
        WHERE datname=%s
        LIMIT 1
        """,
        (db_name,),
    )

    return cursor.fetchone() is not None


@pytest.fixture(scope="module")
def app() -> Iterator[Flask]:
    app = create_app("testing")
    app.test_client_class = FlaskLoginClient

    with app.app_context():
        yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def create_user():
    fake = faker.Faker()
    admin_role = db.session.query(Role).filter(Role.name == "Administrator").one()

    def inner(username=None, password=None, email=None, is_admin=False):
        username = username or fake.user_name()
        password = password or fake.password()
        email = email or fake.company_email()

        user = User.create(
            username=username,
            name=fake.name(),
            email=email,
            password=password,
        )

        if is_admin:
            user.roles = [admin_role]

        return user, password

    return inner


@pytest.fixture()
def create_story(create_user):
    fake = faker.Faker()
    default_fandom = (
        db.session.query(Fandom).filter(Fandom.name == "Original Work").one()
    )

    def inner(author=None, fandom=None, nb_chapters=1):
        fandom = fandom or default_fandom

        if author is None:
            author, _ = create_user()

        story = Story.create(
            title=fake.sentence(),
            summary=" ".join(fake.sentences(nb=5)),
            total_chapters=nb_chapters,
            author=author,
            fandom=[fandom],
            commit=False,
        )

        for chapter in range(nb_chapters):
            Chapter.create(
                story=story,
                title=fake.sentence(),
                summary=" ".join(fake.sentences(nb=3)),
                nb=(chapter + 1),
                content=fake.text(max_nb_chars=3000),
                commit=False,
            )

        return story

    return inner


@pytest.fixture()
def logged_in(client, user, password):
    return client.post(
        "/login",
        data={"username": user.username, "password": password},
        follow_redirects=True,
    )


@pytest.fixture(scope="module")
def database():
    with postgres_cursor() as pg_cur:
        if not database_exists(pg_cur, TestingConfig.POSTGRES_DB):
            pg_cur.execute(f"CREATE DATABASE {TestingConfig.POSTGRES_DB}")

        yield
        pg_cur.execute(f"DROP DATABASE {TestingConfig.POSTGRES_DB} (FORCE)")


@pytest.fixture(scope="module")
def migrations(database, app):
    alembic_config = app.extensions["migrate"].migrate.get_config()

    with db.engine.connect() as conn:
        alembic_config.attributes["connection"] = conn
        alembic.command.upgrade(alembic_config, "head")


@pytest.fixture(autouse=True)
def transaction(migrations):
    conn = db.engine.connect()
    trans = conn.begin()

    db.session.remove()
    db.session.configure(bind=conn)
    db.session().begin_nested()

    @event.listens_for(db.session, "after_transaction_end")
    def end_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            db.session().expire_all()
            db.session().begin_nested()

    yield conn

    db.session.remove()
    trans.rollback()
