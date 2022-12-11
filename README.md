# To-Do List API

Create a virtual environment with Python 3.8 and activate it:

```bash
# For Windows 10 (with already installed Python 3.8 interpreter)
py -3.8 -m venv "venv"
.\venv\Scripts\activate
```

Install dependencies while virtual environment is active:

```
pip install flask flask_sqlalchemy flask-restx flask_login 
```

How to run (while virtual environment is active):

```
flask --app .\main.py run
```

Useful links:

* [Flask](https://flask.palletsprojects.com/en/2.2.x/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
* [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/index.html)
