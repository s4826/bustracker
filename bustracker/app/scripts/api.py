"""Functions to interface with MBTA v3 API"""

import time
from collections import OrderedDict

import requests

from . import gtfs_realtime_pb2
from .cache_decorator import Cache
from .constants import TRIP_UPDATES
from .utils import build_json_request_url


def get_all_route_ids():
    """Get a list of all available route ids from the MBTA"""
    url = build_json_request_url("routes", fields=["id"])
    r = requests.get(url)
    return [route["id"] for route in r.json()["data"]]


def build_route_dict(route_id, direction_id):
    """
    Create a dictionary object and populate it with all stops on
    this route/direction

    :param route_id: MBTA route id
    :param direction_id: Travel direction, 0 (Outbound), or 1 (Inbound)
    """
    route_dict = OrderedDict()

    if not isinstance(route_id, str):
        route_id = str(route_id)

    filter_dict = {"route": route_id, "direction_id": direction_id}
    url = build_json_request_url("stops", filter_dict)
    r = requests.get(url)
    for stop in r.json()["data"]:
        route_dict[stop["id"]] = stop["attributes"]["name"]

    return route_dict


# protobuf api calls


@Cache(seconds=15)
def get_trip_updates():
    """
    Query the MBTA protobuf feed for all trip updates.

    URL: 'https://cdn.mbta.com/realtime/TripUpdates.pb'
    """
    res = []

    feed = gtfs_realtime_pb2.FeedMessage()
    r = requests.get(TRIP_UPDATES)
    feed.ParseFromString(r.content)
    for entity in feed.entity:
        res.append(entity)
    return res


def get_arrival_times(route_id, direction_id, stop_id):
    """
    Get arrival times for a route/direction/stop combination.

    :param route_id: MBTA route id
    :param direction_id: Travel direction, 0 (Outbound), or 1 (Inbound)
    :param stop_id: MBTA stop id
    """
    res = []

    route_id = str(route_id)
    direction_id = int(direction_id)
    stop_id = str(stop_id)

    updates = get_trip_updates()
    direction_updates = filter(
        lambda x: x.trip_update.trip.direction_id == direction_id
        and x.trip_update.trip.route_id == route_id,
        updates,
    )
    for du in direction_updates:
        for stop_time_update in du.trip_update.stop_time_update:
            if (
                stop_time_update.HasField("arrival")
                and stop_time_update.stop_id == stop_id
            ):
                res.append(stop_time_update.arrival.time - int(time.time()))
    return res
