# switches
A web page of switches that don't do anything at all

## Installation and Running
You will need a python installation and preferable a virtualenv to keep things separated from your system python.

* Get Pip *
	`https://pip.pypa.io/en/latest/installing.html`
* Install virtualenv *
	`pip install virtualenv`
* Create a virtualenv *
	`cd /path/to/project/`
	`virtualenv venv`
* Install third party packages into your virtualenv *
	`venv/bin/activate`
	`pip --version` should be pointing at your virtualenv
	`pip install -r requirements.txt`
* Create the database *
	`ipython`
	`from switches import db`
	`db.create_all()`
	`exit()`
* Start up the server *
	`python --version` should be your virtualenv python (how cool!)
	`python switches.py`
* Go to http://localhost:5000/ to see your hard work


## How it works
The switches.py file is the web server which has different "web pages". These are all of the functions which have `@app.route` on them. The `Switch` model is a database table basically. Your database is just the one file called `data.sqlite3` which `create_all` made for you.

The templates/index.html is a jinja2 template (AKA a html file with some curly brackets in it). The flask app populates the template when the page is loaded. The javascript at the bottom changes the page once it has been loaded. We add some click handlers to the delete button and the toggle switch.
