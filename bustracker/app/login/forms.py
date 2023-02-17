"""Login and registration forms"""

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import Email, EqualTo, InputRequired, Length


class LoginForm(FlaskForm):
    """Login form"""

    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), Length(8, 50)])
    remember = BooleanField("Keep me logged in")
    submit = SubmitField("Log In")


class RegisterForm(FlaskForm):
    """Registration form"""

    email = StringField("Email (Username)", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(8, 50)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            Length(8, 50),
            EqualTo("password", message="Passwords do not match."),
        ],
    )
    submit = SubmitField("Register")


class ResendConfirmation(FlaskForm):
    """Confirmation email form"""

    email = StringField("Email", validators=[InputRequired(), Email()])
    submit = SubmitField("Submit")
