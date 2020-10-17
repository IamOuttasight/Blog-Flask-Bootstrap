db_name = 'blog' # Set your own database name if needed
host = 'localhost'
user = 'root' # Set your MySQL login
password = 'toor' # Set your MySQL password

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 2 and sys.argv[1] == 'db':
        import MySQLdb

        db = MySQLdb.connect(
            host,
            user,
            password,
        )
        cur = db.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS {} CHARACTER SET utf8 COLLATE utf8_unicode_ci;".format(db_name))
        db.commit()
        cur.close()
        db.close()
        print("MySQL database '{}' was set successfully.".format(db_name))
    
    elif len(sys.argv) == 2 and sys.argv[1] == 'admin':
        from app import user_datastore
        from models import User, Role
        import getpass
        import sys

        username = str(input("Enter Username: "))
        email = str(input("Enter email: "))
        password = getpass.getpass("Enter password: ")
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
            role = user_datastore.create_role(name='admin', description='administrator')
        
        user_datastore.add_role_to_user(user, role)
        user_datastore.commit()
        print("Now you can log in as admin.")
    else:
        print("Usage: python3 create.py [option]\nOptions: admin, db")
