from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from models import Post
from models import Tag
from .forms import PostForm
from app import db


blog = Blueprint('blog', __name__, template_folder='templates')


@blog.route('/create/', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tags = request.form.getlist('tags')
        try:
            post = Post(title=title, body=body)
            for title in tags:
                tag = Tag.query.filter(Tag.title==title).first()
                post.tags.append(tag)
            db.session.add(post)
            db.session.commit()
        except:
            print('Something went wrong')
        return redirect(url_for('blog.index'))

    form = PostForm()
    return render_template('blog/create_post.html', form=form)


@blog.route('/')
def index():
    q = request.args.get('q', '')
    if q:
        posts = Post.query.filter(
            Post.title.contains(q) | Post.body.contains(q)
            ).all()
    else:
        posts = Post.query.order_by(Post.created.desc())
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