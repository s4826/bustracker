import sys
import time
import json
import requests
import gtfs_realtime_pb2

from config import JSON_API_PREFIX, PB_API_PREFIX, VEHICLE_POSITIONS, TRIP_UPDATES

def build_json_request_url(request_type, filter_dict, fields=None):
    url = JSON_API_PREFIX + request_type 
    url = add_filters(url, filter_dict)
    if fields is not None:
        field_filter = ",".join(fields)
        url += f'&fields[{request_type[:-1]}]=' + field_filter
    return url

def add_filters(url, filter_dict):
    url += "?"
    if 'sort' in filter_dict:
        url += "sort={}&".format(filter_dict['sort'])
    for key in filter_dict:
        if 'sort' != key:
            url += "filter[{}]={}&".format(key, filter_dict[key])
    return url[:-1]


def get_stops_for_route(route_id, direction_id):
    filter_dict = {"route": route_id, "direction_id": direction_id}
    url = build_json_request_url("stops", filter_dict)
    r = requests.get(url)
    return r.json()['data']


def build_route_dict(route_id, direction_id):
    """
    Create a dictionary object and populate it with all stops on
    this route/direction
    """
    route_dict = {}

    if type(route_id) != str:
        route_id = str(route_id)

    filter_dict = {"route": route_id, "direction_id": direction_id}
    url = build_json_request_url("stops", filter_dict)
    r = requests.get(url)
    for stop in r.json()['data']:
        route_dict[stop['id']] = stop['attributes']['name']

    return route_dict


# protobuf api calls

def get_trip_updates_by_route(route):
    if type(route) != str:
        route = str(route)
    res = []

    feed = gtfs_realtime_pb2.FeedMessage()
    r = requests.get(TRIP_UPDATES)
    feed.ParseFromString(r.content)
    for entity in feed.entity:
        if entity.trip_update.trip.route_id == route:
            res.append(entity)
    return res


def get_arrival_times(route_id, direction_id, stop_id):
    """
    Get arrival times at all stops for a route/direction combination.
    """
    res = []

    route_id = str(route_id)
    direction_id = int(direction_id)
    stop_id = str(stop_id)

    updates = get_trip_updates_by_route(route_id)
    direction_updates = filter(lambda x: x.trip_update.trip.direction_id ==
                               direction_id, updates)
    for du in direction_updates:
        trip_id = du.trip_update.trip.trip_id
        for stop_time_update in du.trip_update.stop_time_update:
            if (stop_time_update.HasField('arrival') and
                stop_time_update.stop_id == stop_id):
                    res.append(abs(stop_time_update.arrival.time -
                                        int(time.time())))
    return res

def clock_time_difference(t1, t2):
    return sec_to_clock_time(abs(t1 - t2))


def sec_to_clock_time(seconds):
    h = seconds // 3600
    m = (seconds - h*3600) // 60
    s = (seconds - h*3600 - m*60)
    return f'{m:02}:{s:02}' if h== 0 \
            else f'{h}:{m:02}:{s:02}'

if __name__ == "__main__":
    get_arrival_times(sys.argv[1], sys.argv[2])
