# models.py --- 
# 
# Filename: models.py
# Author: Louise <louise>
# Created: Mon May  4 01:45:09 2020 (+0200)
# Last-Updated: Tue Jul  7 19:06:20 2020 (+0200)
#           By: Louise <louise>
#
from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin
from flask_babel import gettext

from editoggia.database import db
from editoggia.extensions import bcrypt, lm
from editoggia.models.mixins import CRUDMixin

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), nullable=False)

class Role(db.Model, CRUDMixin):
    __tablename__ = 'role'
    
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    users = db.relationship('User', secondary='roles_users', lazy='dynamic',
                            back_populates='roles')
    permissions = db.relationship('Permission', secondary='permissions_roles',
                                  back_populates='roles')

class PermissionsRoles(db.Model):
    __tablename__ = 'permissions_roles'
    
    id = db.Column(db.Integer(), primary_key=True)
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), nullable=False)
    perm_id = db.Column('perm_id', db.Integer(), db.ForeignKey('permission.id'), nullable=False)

class Permission(db.Model, CRUDMixin):
    __tablename__ = 'permission'
    
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    roles = db.relationship('Role', secondary='permissions_roles',
                            back_populates='permissions')

class User(CRUDMixin, UserMixin, db.Model):
    __tablename__ = 'user'

    # Basic info
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    pw_hash = db.Column(db.String(60), nullable=False)

    # More info
    name = db.Column(db.String(128))
    location = db.Column(db.String(128))
    birthdate = db.Column(db.Date())
    gender = db.Column(db.Enum(
        gettext("Woman"),
        gettext("Man"),
        gettext("Other")
    ))
    bio = db.Column(db.String(500), nullable=False, default="")

    # More profile info
    updated_on = db.Column(db.DateTime(),
                           nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # Settings
    language = db.Column(db.String(10), nullable=False, default="")

    # Stories and such
    stories = db.relationship('Story', back_populates='author')
    likes = db.relationship(
        'Story', secondary='user_likes',
        back_populates='user_likes'
    )
    comments = db.relationship('Comment', back_populates='author')
    history = db.relationship('HistoryView', order_by='desc(HistoryView.date)')
    
    # Tracking info
    last_active_at = db.Column(db.DateTime())
    last_active_ip = db.Column(db.String(100))
    last_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer, default=0)
    
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime(),
                             default=datetime.utcnow())
    
    roles = db.relationship(
        'Role',
        secondary='roles_users', lazy='dynamic',
        back_populates='users'
    )                  

    def __init__(self, password, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_password(password)

    def __str__(self):
        return self.name if self.name else self.username
        
    def __repr__(self):
        return '<User #%s:%r>' % (self.id, self.username)

    def set_password(self, password):
        hash_ = bcrypt.generate_password_hash(password, 10).decode('utf-8')
        self.pw_hash = hash_

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pw_hash, password)

    def has_permission(self, permission):
        """
        Check if user has given permission.
        """
        result = self.roles.filter(
            Role.permissions.any(Permission.name == permission)
        ).first()
        
        return result is not None

    def get_from_history(self, story):
        """
        If user has story in its inventory, return the HistoryView
        object. If not, return None.
        """
        from editoggia.models import HistoryView
        
        return db.session.query(HistoryView) \
                             .filter(HistoryView.user_id == self.id) \
                             .filter(HistoryView.story_id == story.id) \
                             .first()

    def add_to_history(self, story, chapter_nb=1):
        """
        A user has loaded a story. Update view time, or
        add to history.
        """
        from datetime import datetime
        from editoggia.models import HistoryView

        existing = self.get_from_history(story)
        
        if existing:
            existing.update(
                date=datetime.utcnow(),
                chapter_nb=chapter_nb
            )
        else:
            # Add a hit to the story
            story.hit()
            HistoryView.create(
                user_id=self.id,
                story=story,
                chapter_nb=chapter_nb
            )

class UserLikes(db.Model):
    __tablename__ = 'user_likes'
    
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), nullable=False)
    story_id = db.Column('story_id', db.Integer(), db.ForeignKey('story.id'), nullable=False)
    
class AnonymousUser(AnonymousUserMixin):
    """
    This defines the anonymous user.
    We define this so we can use the same
    functions everywhere for the permission
    system, and the history.
    """
    def has_permission(self, permission):
        return False
    
    def get_from_history(self, story):
        """
        Because an anonymous user has no history, return None.
        """
        return None
    
    def add_to_history(self, story, chapter_nb=1):
        """
        Add a hit to the story, an anonymous user has no history.
        """
        story.hit()

lm.anonymous_user = AnonymousUser

from editoggia.models.story import Story
