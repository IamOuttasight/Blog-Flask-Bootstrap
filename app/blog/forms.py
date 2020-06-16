from wtforms import Form
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import SelectMultipleField

from models import Post
from models import Tag


class PostForm(Form):
    title = StringField('Title')
    body = TextAreaField('Body')
    tags = SelectMultipleField('Tags', coerce=int)