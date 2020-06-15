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


@blog.route('/<slug>/edit/', methods=['POST', 'GET'])
def edit_post(slug):
    post = Post.query.filter(Post.slug==slug).first()

    print(request.form.items)

    # FIXME: doesn't work for SelectMultipleField.
    # AttributeError: 'str' object has no attribute '_sa_instance_state'
    # There's probably smth wrong with db relations or PostForm.
    if request.method == 'POST':
        form = PostForm(request.form, obj=post)
        form.populate_obj(post) # <- the problem is here
        db.session.commit()
        return redirect(url_for('blog.post_details', slug=post.slug))
    
    form = PostForm(obj=post)
    return render_template('blog/edit_post.html', post=post, form=form)


@blog.route('/')
def index():
    q = request.args.get('q', '')

    page = request.args.get('page')

    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = posts.paginate(page=page, per_page=3)

    return render_template('blog/index.html', pages=pages, q=q)


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