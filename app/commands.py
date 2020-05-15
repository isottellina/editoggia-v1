# commands.py --- 
# 
# Filename: commands.py
# Author: Louise <louise>
# Created: Fri May  8 20:45:27 2020 (+0200)
# Last-Updated: Fri May 15 15:05:29 2020 (+0200)
#           By: Louise <louise>
# 
import click
import flask_migrate
from flask_babel import gettext
from faker import Faker

from app.database import db
from app.user.models import User, Role, Permission

@click.option('--num_users', default=5, help='Number of users.')
def populate_db(num_users):
    """
    Populates the database with fake data from faker
    """
    fake = Faker()
    users = []
    for _ in range(num_users):
        profile = fake.profile([
            "username", "name", "sex", "mail", "birthdate"
        ])
        sex = "Woman" if profile["sex"] == "F" else "Man"
        created = fake.date_this_year()
        
        users.append(
            User(
                username=profile['username'],
                name=profile['name'],
                email=profile['mail'],
                password=fake.password(),
                birthdate=profile['birthdate'],
                location=fake.city(),
                bio=fake.text(),
                gender=sex,

                confirmed_at=created,
                updated_on=fake.date_between(start_date=created),
                last_login_at=fake.date_between(start_date=created),
                last_login_ip=fake.ipv4(),
            )
        )
        
    for user in users:
        db.session.add(user)
    db.session.commit()

def create_db():
    flask_migrate.upgrade()

    admin_role = db.session.query(Role).filter(Role.name=="Administrator") \
                                       .first()
    if not admin_role:
        # Create permissions
        admin_perm = Permission(
            name="admin.ACCESS_ADMIN_INTERFACE",
            description="Can access the admin interface."
        )
        db.session.add(admin_perm)
        
        # Create roles
        admin_role = Role(
            name=gettext("Administrator"),
            description=gettext("Administrator of the website."),
            permissions=[admin_perm]
        )
        db.session.add(admin_role)
        
        # Commit session
        db.session.commit()
    
# Various helpers
@click.argument('username')
def set_admin(username):
    user = db.session.query(User).filter(User.username==username) \
                                 .first()
    admin_role = db.session.query(Role).filter(Role.name=="Administrator") \
                                       .first()
    # If the admin role doesn't exist, we can't add it
    assert admin_role

    user.roles.append(admin_role)
    db.session.commit()

# Register commands
def register_commands(app):
    """
    Register all custom commands for the Flask CLI.
    """
    app.cli.command()(populate_db)
    app.cli.command()(create_db)
    app.cli.command()(set_admin)
