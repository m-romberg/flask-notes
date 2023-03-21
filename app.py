import os

from flask import Flask, request, redirect, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension



from models import db, connect_db, User

from dotenv import load_dotenv
load_dotenv()
API_SECRET_KEY = os.environ["API_SECRET_KEY"]

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///notes_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

debug = DebugToolbarExtension(app)

@app.get("/")
def root():
    """On root, redirect to register"""

    return redirect ("/register")

@app.get("/register")
def register_new_user():


