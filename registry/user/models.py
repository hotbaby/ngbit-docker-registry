
from flask_user import  UserMixin
from ..db import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)

    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    first_name = db.Column(db.String(32), nullable=False, server_default='') 
    last_name = db.Column(db.String(32), nullable=False, server_default='')

    username = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(128), nullable=False, server_default='')

    email = db.Column(db.String(64), nullable=False, unique=True)
    confirm_at = db.Column(db.DateTime)

    rolse = db.relationship('Role', secondary='user_roles',
                           backref=db.backref('users', lazy='dynamic'))


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)
    description = db.Column(db.String(255), server_default='')


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


