# Blog-Flask-Bootstrap
## Description
This web application allows users to register, create posts and tags, manage their own posts (edit/delete) and read posts made by the others. It also contains the admin page, which is made with 
Flask-Admin. Users with the admin role can manage all of the posts and tags despite the authorship. The application also has a search field, pagination, slugs.

* Flask v1.1.2
* Python v3.5.2
* Frontend framework - Bootstrap v4.5.2
* As DBMS was chosen MySQL v5.7.31
* SQLAlchemy v1.3.17
## Installation:
1. At first, you should install _mysql-server_ and _libmysqlclient-dev_ if you don't have it:  
```sudo apt-get install mysql-server libmysqlclient-dev```
2. Clone this repository to your computer and open the folder
3. **Open** file 'app/create.py', set required data (db_name, user, password) and then close the file
4. Install _pipenv_ if you don't have it:  
```pip install pipenv```
5. Install required packages using _pipenv_ (keep staying in the root folder of the project):  
```pipenv install```
6. Launch virtual environment:  
```pipenv shell```
7. Go to 'app/' folder
8. Execute 'create.py' file with 'db' parameter to create a new database:  
```python3 create.py db```
9. Make all the migrations:  
```python3 manage.py db init```  
```python3 manage.py db migrate```  
```python3 manage.py db upgrade```
10. Execute 'create.py' file with 'admin' parameter to create the first admin:  
```python3 create.py admin```
11. Launch 'main.py':  
```python3 main.py```
12. Log in to your admin account on 'http://localhost:5000/admin/'