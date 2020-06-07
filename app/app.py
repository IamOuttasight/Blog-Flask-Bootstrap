from flask import Flask

from config import Configuration
from blog.blueprint import blog


app = Flask(__name__)
app.config.from_object(Configuration)
app.register_blueprint(blog, url_prefix='/blog')