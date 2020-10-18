from create import db_name

class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:toor@localhost/{}'.format(db_name)
    SECRET_KEY = 'extremely-secret-key'

    ### Flask Security ###
    SECURITY_PASSWORD_SALT = 'salt'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_REGISTERABLE = True
    SECURITY_LOGIN_URL = '/login'
    SECURITY_REGISTER_URL = '/register'
    SECURITY_LOGIN_USER_TEMPLATE = 'security/login_user.html'
    SECURITY_REGISTER_USER_TEMPLATE = 'security/register_user.html'
    SECURITY_SEND_REGISTER_EMAIL = False
