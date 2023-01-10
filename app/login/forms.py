from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                    ValidationError)
from wtforms.validators import InputRequired, Length, Email
from email_validator import validate_email

def passwords_match(form, confirm_password):
    if form.password.data != confirm_password.data:
        raise ValidationError('Passwords do not match')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired(),
                                                       Length(8,50)])
    remember = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    email = StringField('Email (Username)',
            validators = [InputRequired(), Email()])
    password = PasswordField('Password',
            validators = [InputRequired(), Length(8,50)])
    confirm_password = PasswordField('Confirm Password',
            validators = [InputRequired(), Length(8,50), passwords_match])
    submit = SubmitField('Register')
