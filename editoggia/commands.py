# commands.py ---
#
# Filename: commands.py
# Author: Louise <louise>
# Created: Fri May  8 20:45:27 2020 (+0200)
# Last-Updated: Wed Jul  8 11:57:04 2020 (+0200)
#           By: Louise <louise>
#
import click
from faker import Faker
from sqlalchemy.sql.expression import func

from editoggia.database import db
from editoggia.models import Chapter, Fandom, Role, Story, User


@click.option("--num_users", default=5, help="Number of users.")
def populate_db_users(num_users):
    """
    Populates the database with fake data from faker
    """
    fake = Faker()

    for _ in range(num_users):
        profile = fake.profile(["username", "name", "sex", "mail", "birthdate"])
        sex = "Woman" if profile["sex"] == "F" else "Man"
        created = fake.date_this_year()

        User(
            username=profile["username"],
            name=profile["name"],
            email=profile["mail"],
            password=fake.password(),
            birthdate=profile["birthdate"],
            location=fake.city(),
            bio=fake.text(),
            gender=sex,
            confirmed_at=created,
            updated_on=fake.date_between(start_date=created),
            last_login_at=fake.date_between(start_date=created),
            last_login_ip=fake.ipv4(),
        ).save()

    db.session.commit()


@click.option("--num_stories", default=10, help="Number of stories")
@click.option("--num_chapters", default=1, help="Number of chapters per stories")
def populate_db_stories(num_stories, num_chapters):
    """
    Populate the database with an appropriate number of stories, written by
    random users. It associates every story with the Original work fandom.
    We don't commit every time because it's so slow.
    """
    fake = Faker()
    fandom = db.session.query(Fandom).filter(Fandom.name == "Original Work").first()
    assert fandom

    for _ in range(num_stories):
        author = db.session.query(User).order_by(func.random()).first()

        story = Story.create(
            title=fake.sentence(),
            summary=" ".join(fake.sentences(nb=5)),
            total_chapters=num_chapters,
            author=author,
            fandom=[fandom],
            commit=False,
        )

        for i in range(num_chapters):
            Chapter.create(
                title=fake.sentence(),
                nb=i + 1,
                summary=" ".join(fake.sentences(nb=5)),
                content=fake.text(max_nb_chars=3000),
                story=story,
                commit=False,
            )

    db.session.commit()


@click.option("--num_users", default=5, help="Number of users")
@click.option("--num_stories", default=10, help="Number of stories")
@click.option("--num_chapters", default=1, help="Number of chapters per stories")
def populate_db(num_users, num_stories, num_chapters):
    """
    Populates the DB both with users and stories.
    """
    populate_db_users(num_users)
    populate_db_stories(num_stories, num_chapters)


# Various helpers
@click.argument("username")
def set_admin(username):
    user = db.session.query(User).filter(User.username == username).first()
    admin_role = Role.get_by_name("Administrator")
    # If the admin role doesn't exist, we can't add it
    assert admin_role

    user.roles.append(admin_role)
    db.session.commit()


# Register commands
def register_commands(app):
    """
    Register all custom commands for the Flask CLI.
    """
    app.cli.command()(populate_db_users)
    app.cli.command()(populate_db_stories)
    app.cli.command()(populate_db)
    app.cli.command()(set_admin)
