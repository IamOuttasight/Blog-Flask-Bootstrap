from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_security import login_required

from models import Post
from models import Tag
from app import db
from .forms import PostForm
from .forms import TagForm


blog = Blueprint('blog', __name__, template_folder='templates')


@blog.route('/create_post/', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        tags = request.form.getlist('tags')
        post = Post(title=title, body=body)
        post.add_tags(tags)

        return redirect(url_for('blog.index'))

    form = PostForm()
    form.tags.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    return render_template('blog/create_post.html', form=form)


@blog.route('/<slug>/edit/', methods=['POST', 'GET'])
@login_required
def edit_post(slug):
    post = Post.query.filter(Post.slug==slug).first_or_404()

    if request.method == 'POST':
        post.title = request.form['title']
        post.body = request.form['body']
        tags = request.form.getlist('tags')
        post.add_tags(tags)

        return redirect(url_for('blog.post_details', slug=post.slug))
    
    form = PostForm(obj=post)
    form.tags.choices = [(tag.id, tag.title) for tag in Tag.query.all()]
    form.tags.data = [tag.id for tag in post.tags]
    return render_template('blog/edit_post.html', post=post, form=form)


# posts must be BaseQuery
def _paginate(page, posts):
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    pages = posts.paginate(page=page, per_page=3)
    return pages


@blog.route('/')
def index():
    q = request.args.get('q', '')
    page = request.args.get('page')

    if q:
        posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
    else:
        posts = Post.query.order_by(Post.created.desc())

    pages = _paginate(page, posts)
    return render_template('blog/index.html', pages=pages, q=q)


@blog.route('/<slug>/')
def post_details(slug):
    post = Post.query.filter(Post.slug==slug).first_or_404()
    tags = post.tags
    return render_template('blog/post_details.html', post=post, tags=tags)


@blog.route('/tag/<slug>/')
def tag_details(slug):
    page = request.args.get('page')
    tag = Tag.query.filter(Tag.slug==slug).first_or_404()
    posts = tag.posts.filter()
    pages = _paginate(page, posts)
    return render_template('blog/tag_details.html', tag=tag, pages=pages)


@blog.route('/create_tag/', methods=['POST', 'GET'])
@login_required
def create_tag():
    if request.method == 'POST':
        title = request.form['title']
        tag = Tag(title=title)
        db.session.add(tag)
        db.session.commit()
        return redirect(url_for('blog.tags_list'))

    form = TagForm()
    return render_template('blog/create_tag.html', form=form)


@blog.route('/tags/')
def tags_list():
    tags = Tag.query.all()
    return render_template('blog/tags_list.html', tags=tags)