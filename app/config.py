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
    import getpass
    import sys

    username = str(input("Enter Username: "))
    email = str(input("Enter email: "))
    password = getpass.getpass("Enter password: ") #str(input("Enter password: "))
    confirm = getpass.getpass("Confirm password: ")
    
    if password != confirm:
        sys.exit("ERROR: Confirmation failed.")
    user_by_username = Role.query.filter(User.username==username).first()
    user_by_email = Role.query.filter(User.email==email).first()
    if user_by_username:
        sys.exit("ERROR: Username is already taken.")
    elif user_by_email:
        sys.exit("ERROR: Email is already taken.")
    else:
        user = user_datastore.create_user(username=username, email=email, password=password)

    role = Role.query.filter(Role.name=='admin').first()
    if not role:
        role = user_datastore.create_role('admin', 'administrator')
    
    user_datastore.add_role_to_user(user, role)
    user_datastore.commit()
    print("Now you can enter the admin page.")