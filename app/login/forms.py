"""Login and registration forms"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    """Login form"""
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password',
                             validators=[InputRequired(), Length(8, 50)])
    remember = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    """Registration form"""
    email = StringField('Email (Username)',
                        validators=[InputRequired(), Email()])
    password = PasswordField('Password',
                             validators=[InputRequired(), Length(8, 50)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[
                                       InputRequired(),
                                       Length(8, 50),
                                       EqualTo('password',
                                            message='Passwords do not match.')])
    submit = SubmitField('Register')
