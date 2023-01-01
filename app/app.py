from flask import Flask, render_template, g, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

from dotenv import load_dotenv
from os import environ

from app.forms import *
from app.scripts.cache_decorator import Cache
import app.scripts.api as api

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = environ['SECRET_KEY']

bootstrap = Bootstrap(app)
directions = {'outbound': 0, 'inbound': 1}

@app.before_request
def create_forms():
    # don't re-create forms on requests for static content
    if request.endpoint != None and 'static' not in request.endpoint:
        if 'route_form' not in g:
            g.route_form = create_route_form()
        if 'direction_form' not in g:
            g.direction_form = create_direction_form()


@app.route('/', methods = ['GET', 'POST'])
@app.route('/routes/<route_id>', methods = ['GET', 'POST'])
def index(route_id=None, direction=None, stop_id=None):
    if route_id is not None and direction is not None:

        dir_id = directions[direction]
        route_stops = api.build_route_dict(route_id, dir_id)

        return render_template('choose_dir.html', route_form=g.route_form,
                               direction_form=g.direction_form)

    else:
        return render_template('choose_route.html', route_form=g.route_form)


@app.route('/routes/<route_id>/<direction>', methods = ['GET', 'POST'])
def choose_stop(route_id, direction):
    dir_id = directions[direction]
    route_stops = api.build_route_dict(route_id, dir_id)
    return render_template('choose_stop.html',
                           route_form=g.route_form,
                           direction_form=g.direction_form,
                           route_stops=route_stops)


@app.route('/routes/<route_id>/<direction>/<stop_id>', methods = ['GET'])
def get_stop_predictions(route_id, direction, stop_id):
    dir_id = directions[direction]
    predictions = sorted(api.get_arrival_times(route_id, dir_id, stop_id))
    return render_template('show_stop_times.html', route_form=g.route_form,
                           direction_form=g.direction_form,
                           predictions=predictions)


@Cache(seconds=30)
def create_route_form():
    route_form = RouteForm()
    route_choices = [''] + api.get_all_route_ids()
    route_form.route_list.choices = route_choices
    return route_form


@Cache(seconds=30)
def create_direction_form():
    dir_choices = [''] + list(directions.keys())
    direction_form = DirectionForm()
    direction_form.dir_list.choices = dir_choices
    return direction_form

