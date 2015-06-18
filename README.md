# switches
A web page of switches that don't do anything at all [ ![Codeship Status for Smirl/teaflask](https://www.codeship.io/projects/2d362f80-f7bf-0132-941f-76fcd0eb4f4a/status)](https://www.codeship.io/projects/86425)

![switches-screenshot](https://cloud.githubusercontent.com/assets/5792870/8129223/d69ebed0-10fe-11e5-9827-de72edfd54b9.png)

## Installation and Running

You will need a python installation and preferable a virtualenv to keep things separated from your system python. First you should get Pip, https://pip.pypa.io/en/latest/installing.html. Now lets set things up.

We will create a virtual version of python which is separate from the your main python and other projects. Lets put it inside the switches repo, never commit this to git though. The last step here where we activate the virtualenv will change depending on your platform.

```sh
$ cd switches
$ pip install virtualenv
$ virtualenv venv
$ source venv/Scripts/activate
```

Now that we are activated in the virtualenv you should the name of it on your prompt. Lets install the python requirements. The first 2 commands should just point at your virtualenv, this is just so you can see what is happening.

```sh
(venv)$ python --version
(venv)$ pip --version
(venv)$ pip install -r requirements-dev.txt
```


Create the database. This only needs to be done the once not everytime you run the app.

```sh
(venv)$ ipython
>from switches import db
>db.create_all()
>exit()
```

Start up the server with the flask debug server.

```sh
(venv)$ python switches.py
```

In production we should use something better like `gunicorn`. `gunicorn` will also be installed when you ran `pip install -r` so you can try that too.

```sh
(venv)$ gunicorn switches:app --log-file - --log-level debug --port 5000
```

Go to http://localhost:5000/ to see your hard work

## Heroku
This has been deployed to heroku and you can see the master branch at http://intense-depths-2389.herokuapp.com. The Procfile runs the gunicorn server with some logging. Heroku deployment uses postgresql not sqlite3. This is configured with the `DATABASE_URL` environment variable which is set in heroku. For development sqlite3 is fine and you do not need to install the `psycopg2` python package.

## How it works
The switches.py file is the web server which has different "web pages". These are all of the functions which have `@app.route` on them. The `Switch` model is a database table basically. Your database is just the one file called `switches.sqlite3` which `create_all` made for you.

The `templates/index.html` is a jinja2 template (AKA a html file with some curly brackets in it). The flask app populates the template when the page is loaded. The javascript at the bottom changes the page once it has been loaded. We add some click handlers to the delete button and the toggle switch.
