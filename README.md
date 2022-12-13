# To-Do List API

Create a virtual environment with Python 3.8 and activate it:

```bash
# For Windows 10 PowerShell (with already installed Python 3.8 interpreter)
py -3.8 -m venv "venv"
.\venv\Scripts\activate

# For Ubuntu 20.04 Bash
python3.8 -m install virtualenv
python3.8 -m virtualenv venv
chmod +x ./venv/bin/activate
source ./venv/bin/activate
```

Requirements:

* **Python** version ``3.8.10`
* **Flask** version `2.2.2`
* **Flask-Login** version `0.6.2`
* **Flask-Migrate** version `4.0.0`
* **flask-restx** version `1.0.3`
* **Flask-SQLAlchemy** version `3.0.2`

Install dependencies while virtual environment is active:

```
# Install versions according to requirements
pip install -r requirements.txt

# or (This might cause version problems)
pip install flask flask_sqlalchemy flask-migrate flask-restx flask_login
```

How to run (while virtual environment is active):

```
flask --app .\main.py run
```

Useful links:

* [Flask](https://flask.palletsprojects.com/en/2.2.x/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/index.html)
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
