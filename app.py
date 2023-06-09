import os

from flask import Flask, redirect, render_template, flash, session
from werkzeug.exceptions import Unauthorized
from flask_debugtoolbar import DebugToolbarExtension


from models import db, connect_db, User, Note
from forms import RegisterUserForm, LoginForm, CSRFProtectForm

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

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_new_user():
    """Get form to register new user or handle form """

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
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

        session["username"] = user.username
        flash(f"Thanks, {user.first_name}!")

        return redirect(f'/users/{user.username}')

    else:
        return render_template("register_user_form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Get form to login and handle login attempts"""

    if "username" in session:
        username = session["username"]
        return redirect(f'/users/{username}')

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username

            flash(f"Welcome back, {user.first_name}!")
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username/password combination."]
            return render_template("login.html", form=form)

    else: #TODO: omit and dedent
        return render_template("login.html", form=form)


# @app.get('/users/<username>')
# def display_user(username):
#     """Display the user detail page if user is logged in or redirect to root"""


#     if "username" not in session or session['username'] != username:
#         flash(f"Sorry, only {username} may access this page.")
#         #TODO: raise unauthorized() instead of flashing and redirecting
#         return redirect("/")

#     form = CSRFProtectForm()
#     user = User.query.get_or_404(username)

#     return render_template("user_details.html", user=user, form=form)

@app.post('/logout')
def logout():
    """Log out a user"""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)
    #TODO: raise an unauthorized error here
    # Import unauthorized error
        return redirect("/")
    else:
        raise Unauthorized()


###################################Notes Routes#################################

@app.get('/users/<username>')
def display_user(username):
    """Display the user detail page if user is logged in or redirect to root"""


    if "username" not in session or session['username'] != username:
        raise Unauthorized()

    form = CSRFProtectForm()
    user = User.query.get_or_404(username)

    return render_template("user_details.html", user=user, form=form)

@app.post('/users/<username>/delete')
def delete_user(username):
    """Delete the user and all notes."""

    if "username" not in session or session['username'] != username:
        raise Unauthorized()

    form = CSRFProtectForm()

    if form.validate_on_submit():
        #find the user via query
        user = User.query.get_or_404(username)
        #delete all matching notes
        Note.query.filter(Note.owner==user.username).delete()
        db.session.delete(user)
        db.session.commit()

        session.pop("username", None)
        return redirect("/")
    else:
        raise Unauthorized()