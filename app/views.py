"""Main views for route and stop selection"""

from flask import render_template, g, request, session, Blueprint

from log_config import get_logger
from .forms import RouteForm, DirectionForm, SelectStopForm
from .scripts.cache_decorator import Cache
from .scripts import api

debug_logger = get_logger('debug')
error_logger = get_logger('error')

app_bp = Blueprint('app_bp', __name__)

directions = {'outbound': 0, 'inbound': 1}


@app_bp.before_request
def create_forms():
    """Before request hook to save and reload previously created forms"""
    # don't re-create forms on requests for static content
    if request.endpoint is not None and 'static' not in request.endpoint:
        if 'route_form' not in g:
            g.route_form = create_route_form()
        if 'direction_form' not in g:
            g.direction_form = create_direction_form()
        if 'stop_form' not in g:
            g.stop_form = create_stop_form()


@app_bp.route('/', methods=['GET', 'POST'])
@app_bp.route('/routes/<route_id>', methods=['GET', 'POST'])
def index(route_id=None):
    """Main app view"""
    if route_id is not None:
        return render_template('choose_dir.html', route_form=g.route_form,
                               direction_form=g.direction_form)
    return render_template('choose_route.html', route_form=g.route_form)


@app_bp.route('/routes/<route_id>/<direction>', methods=['GET', 'POST'])
def choose_stop(route_id, direction):
    """Stop selection view"""
    dir_id = directions[direction]
    route_dir_id = str(route_id) + '-' + str(dir_id)
    try:
        session[route_dir_id] = api.build_route_dict(route_id, dir_id)
        g.stop_form.stop_list.choices = [('', '')] + \
            list(session[route_dir_id].items())
        debug_logger.info('Added %s dictionary to session object', route_dir_id)
    except KeyError:
        error_logger.exception('%s not in session object', route_dir_id)
    return render_template('choose_stop.html',
                           route_form=g.route_form,
                           direction_form=g.direction_form,
                           stop_form=g.stop_form)


@app_bp.route('/routes/<route_id>/<direction>/<stop_id>', methods=['GET'])
def get_stop_predictions(route_id, direction, stop_id):
    """
    Prediction display view

    :param route_id: MBTA route id
    :param direction: Travel direction, either 0 (Outbound) or 1 (Inbound)
    :param stop_id: MBTA stop id
    """
    dir_id = directions[direction]

    # 'route_dir_id' is used to save route dictionaries in the
    # session object, in the form '{id}-{direction}' (e.g. '77-1')
    route_dir_id = str(route_id) + '-' + str(dir_id)
    if route_dir_id not in session:
        session[route_dir_id] = api.build_route_dict(route_id, dir_id)
    try:
        g.stop_form.stop_list.choices = [('', '')] + \
            list(session[route_dir_id].items())
    except KeyError:
        error_logger.exception('%s not in session object', route_dir_id)

    predictions = sorted(api.get_arrival_times(route_id, dir_id, stop_id))
    return render_template('show_stop_times.html', route_form=g.route_form,
                           direction_form=g.direction_form,
                           stop_form=g.stop_form,
                           predictions=predictions,
                           stop_name=session[route_dir_id][stop_id])


@Cache(seconds=30)
def create_route_form():
    """Route form creator"""
    route_form = RouteForm()
    route_choices = [''] + api.get_all_route_ids()
    route_form.route_list.choices = route_choices
    return route_form


@Cache(seconds=30)
def create_direction_form():
    """Direction form creator"""
    dir_choices = [''] + list(directions.keys())
    direction_form = DirectionForm()
    direction_form.dir_list.choices = dir_choices
    return direction_form


def create_stop_form():
    """Stop form creator"""
    stop_form = SelectStopForm()
    return stop_form
