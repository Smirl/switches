"""
Switches allows persistent boolean state to be displayed as a comical switch.

A simple flask app with a sqlite3 database backend.
"""

import logging
import os
import sys
from datetime import datetime

from flask import Flask, jsonify, redirect, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

# We need to create app at module level so we have it, pretty nasty
# proper way would be to make this whole app not in one file. That isn't as
# fun though.

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or "ghjkl;IU3jnca;hFIAZ"
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["TESTING"] = os.environ.get("TESTING", False) == "True"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///switches.sqlite"
)
app.config["SQLALCHEMY_DATABASE_URI"] = app.config["SQLALCHEMY_DATABASE_URI"].replace(
    "postgres://", "postgresql://"
)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


class Switch(db.Model):
    """The on off value in the database."""

    __tablename__ = "switches"

    id_ = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(64), nullable=False, unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)
    value = db.Column(db.Boolean, default=False)

    def to_dict(self):
        """A dict representation for using with json."""
        return {
            "id_": self.id_,
            "slug": self.slug,
            "created": self.created,
            "updated": self.updated,
            "value": self.value,
        }

    def flip(self):
        """Toggle the switch. and commit it."""
        self.value = not self.value
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def on_changed_value(target, value, oldvalue, initiator):
        """The function to call when the "value" changes."""
        target.updated = datetime.utcnow()
        db.session.add(target)
        db.session.commit()


# This is the event listener
db.event.listen(Switch.value, "set", Switch.on_changed_value)


@app.route("/")
def homepage():
    """Render the homepage template. Also pass in all of the switches."""
    switches = Switch.query.all()
    return render_template("index.html", switches=switches)


@app.route("/api/flip/<id_>", methods=["POST"])
def api_flip(id_):
    """Flip the switch with the given id. Return new state of that switch."""
    s = Switch.query.get_or_404(id_)
    s.flip()
    return jsonify(s.to_dict())


@app.route("/api/add", methods=["POST"])
def api_add():
    """
    Add a new Switch using the slug given in the form.

    Note this isn't really an API method, it returns a redirect to the homepage.
    """
    s = Switch(slug=request.form["slug"].strip())
    db.session.add(s)
    db.session.commit()
    return redirect("/")


@app.route("/api/delete/<id_>", methods=["POST"])
def api_delete(id_):
    """Delete the Switch with the id. Delete something twice is ok."""
    s = Switch.query.get(id_)
    if s is not None:
        db.session.delete(s)
        db.session.commit()
        message = "Deleted {}".format(id_)
    else:
        message = "Did not find {}".format(id_)
    return jsonify({"message": message})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
