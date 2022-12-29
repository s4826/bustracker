from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

from dotenv import load_dotenv
from os import environ

from app.forms import *
import app.scripts.api as api

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sean'

bootstrap = Bootstrap(app)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/routes/<route_id>', methods = ['GET', 'POST'])
@app.route('/routes/<route_id>/<direction>', methods = ['GET', 'POST'])
def index(route_id=None, direction=None):
    route_form = RouteForm()
    route_choices = [""] + api.get_all_route_ids()
    route_form.route_list.choices = route_choices

    if route_id is not None:
        route_form.route_list.value = route_id
        dir_choices = ["", "Outbound", "Inbound"]
        direction_form = DirectionForm()
        direction_form.dir_list.choices = dir_choices

        if direction is not None:
            dir_id = 0 if direction == "Outbound" else 1
            route_stops = api.build_route_dict(route_id, dir_id)
            print(route_stops)
            return render_template('choose_stop.html',
                                   route_form=route_form,
                                   direction_form=direction_form,
                                   route_stops=route_stops)

        return render_template('choose_dir.html', route_form=route_form,
                               direction_form=direction_form)

    else:
        return render_template('choose_route.html', route_form=route_form)

@app.route('/stops/<stop_id>', methods = ['GET'])
def stop_predictions(stop_id):
    pass
