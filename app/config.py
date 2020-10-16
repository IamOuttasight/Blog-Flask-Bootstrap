class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:toor@localhost/blog'
    SECRET_KEY = 'extremely-secret-key'

    ### Flask Security
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'bcrypt'


if __name__ == "__main__":
    from app import user_datastore
    from models import User, Role

    email = str(input("Enter email:\n"))
    password = str(input("Enter password:\n"))

    user = Role.query.filter(User.email==email).first()
    if user:
        raise Exception("Email is already taken")
    else:
        user = user_datastore.create_user(email=email, password=password)

    role = Role.query.filter(Role.name=='admin').first()
    if not role:
        role = user_datastore.create_role('admin', 'administrator')
    
    user_datastore.add_role_to_user(user, role)
    user_datastore.commit()
    print("Now you can enter the admin page.")