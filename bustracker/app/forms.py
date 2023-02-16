"""Main forms for trip selection"""

from flask_wtf import FlaskForm
from wtforms import SelectField


class RouteForm(FlaskForm):
    """Route selection form"""
    route_list = SelectField("Choose a route", validate_choice=True)


class DirectionForm(FlaskForm):
    """Direction selection form"""
    dir_list = SelectField("Direction", validate_choice=True, default="")


class SelectStopForm(FlaskForm):
    """Stop selection form"""
    stop_list = SelectField("Choose a stop", validate_choice=True)
