from flask import Blueprint
from flask import render_template

from models import Post


blog = Blueprint('blog', __name__, template_folder='templates')


@blog.route('/')
def index():
    posts = Post.query.all()
    return render_template('blog/index.html', posts=posts)


@blog.route('/<slug>/')
def post_details(slug):
    post = Post.query.filter(Post.slug==slug).first()
    return render_template('blog/post_details.html', post=post)   