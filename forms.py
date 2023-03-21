"""Forms for notes app."""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length, URL, Optional

class RegisterUserForm(FlaskForm):
    """Form for registering new user."""

    username = StringField(
        "Username",
        validators=[InputRequired(message="Please enter a username.")]
    )

    password = StringField(
        "Password",
        validators=[InputRequired(message="Please enter a password.")]
    )
    email = StringField(
        "Email",
        validators=[
            InputRequired(message="Please enter an email."),
            URL(message="Please enter a valid email.")]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired(message="Please enter a first name.")]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(message="Please enter a last name.")]
    )
