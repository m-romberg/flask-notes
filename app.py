import os

from flask import Flask, request, redirect, render_template, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension



from models import db, connect_db, User
from forms import RegisterUserForm

from dotenv import load_dotenv
load_dotenv()
API_SECRET_KEY = os.environ["API_SECRET_KEY"]

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = API_SECRET_KEY

connect_db(app)

debug = DebugToolbarExtension(app)

@app.get("/")
def root():
    """On root, redirect to register"""

    return redirect ("/register")

@app.route("/register", methods=["GET", "POST"])
def register_new_user():
    """Get form to register new user or handle form """

    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data,
        password = form.password.data,
        email = form.email.data,
        first_name = form.first_name.data,
        last_name = form.last_name.data

        user = User.register(
            username,
            password,
            email,
            first_name,
            last_name
        )

        db.session.add(user)
        db.session.commit()
        flash(f"Thanks, {user.first_name}!")
        return redirect('/secret')

    else:
        return render_template("register_user_form.html", form=form)

@app.get('/secret')
def return_secret():
    return 'HELLO'





