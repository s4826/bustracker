from flask_wtf import FlaskForm
from wtforms import SelectField


class RouteForm(FlaskForm):
    route_list = SelectField("Choose a route", validate_choice=True)


class DirectionForm(FlaskForm):
    dir_list = SelectField("Direction", validate_choice=True, default="")


class SelectStopForm(FlaskForm):
    stop_list = SelectField("Choose a stop", validate_choice=True)
