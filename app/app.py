from flask import Flask
from flask import redirect
from flask import url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_migrate import MigrateCommand
from flask_script import Manager
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user
from flask_wtf.csrf import CSRFProtect

from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

### CSRF ###
csrf = CSRFProtect(app)

### ORM ###
db = SQLAlchemy(app)

### Database migrations ###
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

### Admin ###
from models import *


class AdminMixin():
    def is_accessible(self):
        return current_user.has_role('admin')
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        if type(model) is Post and not model.created:
            model.gen_slug()
            model.created = datetime.now()
        elif type(model) is Tag:
            model.gen_slug()
        return super().on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['tags', 'title', 'body']


class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'posts']


class UserAdminView(AdminMixin, BaseModelView):
    form_columns = ['email', 'active', 'roles']


class RoleAdminView(AdminMixin, BaseModelView):
    form_columns = ['name', 'description', 'users']


admin = Admin(app, 'FlaskApp', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(RoleAdminView(Role, db.session))
admin.add_link(MenuLink(name='Logout', category='', url="/logout"))

### Flask Security ###
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)