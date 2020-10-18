from wtforms import Form
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import SelectMultipleField
from wtforms import validators

from models import Post
from models import Tag


class PostForm(Form):
    title = StringField('Title', [validators.Length(min=5, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])
    tags = SelectMultipleField('Tags', coerce=int)


class TagForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=20)])