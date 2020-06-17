from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

### ORM ###
db = SQLAlchemy(app)

### Database migrations ###
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

### Admin ###
from models import *
admin = Admin(app)
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))
