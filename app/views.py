from flask import render_template, g, request, session, Blueprint

import logging
from logging.config import dictConfig
from log_config import log_config

from .forms import *
from .scripts.cache_decorator import Cache
from .scripts import api

dictConfig(log_config)
debug_logger = logging.getLogger('debug')
error_logger = logging.getLogger('error')

from app.models import Stop, User

app_bp = Blueprint('app_bp', __name__)

directions = {'outbound': 0, 'inbound': 1}

@app_bp.before_request
def create_forms():
    # don't re-create forms on requests for static content
    if request.endpoint != None and 'static' not in request.endpoint:
        if 'route_form' not in g:
            g.route_form = create_route_form()
        if 'direction_form' not in g:
            g.direction_form = create_direction_form()
        if 'stop_form' not in g:
            g.stop_form = create_stop_form()


@app_bp.route('/', methods = ['GET', 'POST'])
@app_bp.route('/routes/<route_id>', methods = ['GET', 'POST'])
def index(route_id=None, direction=None, stop_id=None):
    if route_id is not None:
        return render_template('choose_dir.html', route_form=g.route_form,
                               direction_form=g.direction_form)

    else:
        return render_template('choose_route.html', route_form=g.route_form)


@app_bp.route('/routes/<route_id>/<direction>', methods = ['GET', 'POST'])
def choose_stop(route_id, direction):
    dir_id = directions[direction]
    route_dir_id = str(route_id) + '-' + str(dir_id)
    try:
        session[route_dir_id] = api.build_route_dict(route_id, dir_id)
        g.stop_form.stop_list.choices = [('', '')] + \
            list(session[route_dir_id].items())
        debug_logger.info(f'Added {route_dir_id} dictionary to session object')
    except KeyError:
        error_logger.exception(f'{route_dir_id} not in session object')
    return render_template('choose_stop.html',
                           route_form=g.route_form,
                           direction_form=g.direction_form,
                           stop_form=g.stop_form)


@app_bp.route('/routes/<route_id>/<direction>/<stop_id>', methods = ['GET'])
def get_stop_predictions(route_id, direction, stop_id):
    dir_id = directions[direction]
    route_dir_id = str(route_id) + '-' + str(dir_id)
    if route_dir_id not in session:
        session[route_dir_id] = api.build_route_dict(route_id, dir_id)

    try:
        g.stop_form.stop_list.choices = [('', '')] + \
            list(session[route_dir_id].items())
    except KeyError:
        error_logger.exception(f'{route_dir_id} not in session object')

    predictions = sorted(api.get_arrival_times(route_id, dir_id, stop_id))
    return render_template('show_stop_times.html', route_form=g.route_form,
                           direction_form=g.direction_form,
                           stop_form=g.stop_form,
                           predictions=predictions,
                           stop_name=session[route_dir_id][stop_id])


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


def create_stop_form():
    stop_form = SelectStopForm()
    return stop_form
