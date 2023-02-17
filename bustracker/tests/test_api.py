import json
import os
from collections import OrderedDict

import requests
from app.scripts import api
from app.scripts.constants import INBOUND

test_dir = os.path.dirname(__file__)


class MockJsonResponse:
    def __init__(self, file):
        """
        Construct a mock response object where 'file' is a test
        data file containing the mock response json data.
        """
        self.data_file = file

    def json(self):
        path = os.path.join(test_dir, "data", self.data_file)
        with open(path) as response:
            js_string = response.readline().strip()
        return json.loads(js_string)


class MockProtobufResponse:
    def __init__(self, file):
        path = os.path.join(test_dir, "data", file)
        with open(path) as response:
            self.content = response.readlines.strip()


def test_get_all_route_ids(monkeypatch):
    def mock_get(url):
        return MockJsonResponse("route_ids.json")

    monkeypatch.setattr(requests, "get", mock_get)

    with open(os.path.join(test_dir, "data", "routes"), "r") as routes:
        lines = list(map(lambda s: s.strip(), routes.readlines()))

    assert api.get_all_route_ids() == lines


def test_build_route_dict(monkeypatch):
    def mock_get(url):
        return MockJsonResponse("77in.json")

    monkeypatch.setattr(requests, "get", mock_get)

    d = api.build_route_dict(77, INBOUND)
    assert isinstance(d, OrderedDict)

    with open(os.path.join(test_dir, "data", "77in_dict"), "r") as route_dict:
        stops = list(map(lambda s: s.strip(), route_dict.readlines()))

    stop_dict = OrderedDict()
    for stop in stops:
        key, value = stop.split(", ")
        stop_dict[key] = value

    assert stop_dict == d
