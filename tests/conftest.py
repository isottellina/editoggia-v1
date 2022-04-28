from contextlib import contextmanager
from typing import Iterator

import alembic.command
import faker
from flask.app import Flask
import pytest
import sqlalchemy.exc
import psycopg2
from alembic.runtime.environment import EnvironmentContext
from alembic.script.base import ScriptDirectory
from editoggia import create_app
from editoggia.database import db
from editoggia.config import TestingConfig
from sqlalchemy import event
from sqlalchemy.engine.base import Connection

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
        (db_name,)
    )

    return cursor.fetchone() is not None

@pytest.fixture(scope="module")
def app() -> Iterator[Flask]:
    app = create_app("testing")

    with app.app_context():
        yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def password():
    """
    Returns a random password.
    """
    fake = faker.Faker()
    return fake.password()

@pytest.fixture()
def user(password):
    """
    Returns a created user.
    """
    fake = faker.Faker()

    admin_role = db.session.query(Role).filter(Role.name=="Administrator").one()

    user = User.create(
        username=fake.user_name(),
        name=fake.name(),
        email=fake.company_email(),
        password=password,
    )
    user.roles = [admin_role]

    return user

@pytest.fixture()
def stories(request: pytest.FixtureRequest, user):
    def story(author):
        pass

    nb_stories = request.node.get_closest_marker("nb_stories")
    nb_stories = 2 if nb_stories is None else nb_stories.args[0]

    return [story(user) for _ in range(nb_stories)]

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
