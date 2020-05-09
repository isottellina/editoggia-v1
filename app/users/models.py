# models.py --- 
# 
# Filename: models.py
# Author: Louise <louise>
# Created: Mon May  4 01:45:09 2020 (+0200)
# Last-Updated: Sat May  9 23:59:26 2020 (+0200)
#           By: Louise <louise>
# 
from flask_login import UserMixin

from app.database import db, CRUDMixin
from app.extensions import bcrypt

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), nullable=False)
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), nullable=False)

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    
    permissions = db.relationship('Permission', secondary='permissions_roles',
                                  backref=db.backref('roles', lazy='dynamic'))

class PermissionsRoles(db.Model):
    __tablename__ = 'permissions_roles'
    id = db.Column(db.Integer(), primary_key=True)
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), nullable=False)
    perm_id = db.Column('perm_id', db.Integer(), db.ForeignKey('permission.id'), nullable=False)

class Permission(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

class User(CRUDMixin, UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    # Basic info
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    pw_hash = db.Column(db.String(60), nullable=False)

    # More info
    name = db.Column(db.String(128))
    bio = db.Column(db.Text)
    
    # Tracking info
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer, default=0)
    
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))
    
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
