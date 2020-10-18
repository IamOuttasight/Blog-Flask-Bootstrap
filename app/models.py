from app import db
from app import current_user
from time import time
from datetime import datetime
from slugify import slugify

from flask_security import UserMixin
from flask_security import RoleMixin
import email_validator


post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
    )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    author = db.Column(db.String(30))
    created = db.Column(db.DateTime)

    tags = db.relationship(
        'Tag',
        secondary=post_tags,
        backref=db.backref('posts', lazy='dynamic')
        )

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.gen_slug()
        self.created = datetime.now()
        self.author = current_user.username

    def gen_slug(self):
        if self.title:
            self.slug = slugify(self.title) + '-' + str(int(time()))

    def __repr__(self):
        return '<Post id: {}, Title: {}>'.format(self.id, self.title)

    def add_tags(self, tags):
        if self.tags:
            self.tags = []
        for indx in tags:
            tag = Tag.query.filter_by(id=indx).first()
            self.tags.append(tag)



class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    author = db.Column(db.String(30))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.gen_slug()
        self.author = current_user.username
    
    def gen_slug(self):
        if self.title:
            self.slug = slugify(self.title) + '-' + str(int(time()))

    def __repr__(self):
        return self.title


### Flask Security

users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
    )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship(
        'Role',
        secondary=users_roles,
        backref=db.backref('users', lazy='dynamic')
        )

    def __repr__(self):
        return self.email


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return self.name