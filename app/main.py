from app import app
from app import db
from blog.blueprint import blog
import view


app.register_blueprint(blog, url_prefix='/blog')


if __name__ == "__main__":
    app.run()