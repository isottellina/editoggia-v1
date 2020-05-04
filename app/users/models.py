# models.py --- 
# 
# Filename: models.py
# Author: Louise <louise>
# Created: Mon May  4 01:45:09 2020 (+0200)
# Last-Updated: Mon May  4 03:30:24 2020 (+0200)
#           By: Louise <louise>
# 
from flask_login import UserMixin

from app.extensions import db

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class PermissionsRoles(db.Model):
    __tablename__ = 'permissions_roles'
    id = db.Column(db.Integer(), primary_key=True)
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    perm_id = db.Column('perm_id', db.Integer(), db.ForeignKey('permission.id'))

class Permission(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))
