from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                    ValidationError)
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired(),
                                                       Length(8,50)])
    remember = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')
