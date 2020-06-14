from flask import Blueprint
from flask import render_template
from flask import request

from models import Post
from models import Tag


blog = Blueprint('blog', __name__, template_folder='templates')


@blog.route('/')
def index():
    q = request.args.get('q', '')
    if q:
        posts = Post.query.filter(
            Post.title.contains(q) | Post.body.contains(q)
            ).all()
    else:
        posts = Post.query.all()
    return render_template('blog/index.html', posts=posts)


@blog.route('/<slug>/')
def post_details(slug):
    post = Post.query.filter(Post.slug==slug).first()
    tags = post.tags
    return render_template('blog/post_details.html', post=post, tags=tags)


@blog.route('/tag/<slug>/')
def tag_details(slug):
    tag = Tag.query.filter(Tag.slug==slug).first()
    posts = tag.posts.all()
    return render_template('blog/tag_details.html', tag=tag, posts=posts)