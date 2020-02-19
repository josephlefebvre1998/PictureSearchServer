# Introduction

This project worked with python virtual environment.
Libraries requirements are stored in requirements.txt.

# Set Virtual Environment

To manually create a virtualenv on MacOS and Linux:

```
$ %python-executable% -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

# Start Server

```
$ python manage.py runserver
```

# To apply changes in db 

```
$ python manage.py makemigrations

$ python manage.py migrate --run-syncdb
```
# Heroku migration :
```
$ heroku login

$ heroku run bash -a deep-fashion-server

$ python manage.py migrate --run-syncdb
```