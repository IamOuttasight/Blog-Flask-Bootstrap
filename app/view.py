from app import app
from flask import render_template


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('/security/login_user.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('/security/register_user.html')


@app.errorhandler(404)
def page_not_found(event):
    return render_template('404.html'), 404