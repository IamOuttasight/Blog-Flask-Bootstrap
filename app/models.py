from app import db
from time import time
from datetime import datetime
from slugify import slugify


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.gen_slug()

    def gen_slug(self):
        if self.title:
            self.slug = slugify(self.title) + '-' + str(int(time()))

    def __repr__(self):
        return '<Post id: {}, Title: {}>'.format(self.id, self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.title) + '-' + str(int(time()))

    def __repr__(self):
        return '<Tag id: {}, Title: {}>'.format(self.id, self.title)