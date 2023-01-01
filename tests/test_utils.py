from app.scripts.utils import *
from app.scripts.constants import *

def test_build_json_request_url():
    request = 'routes'
    url_one = build_json_request_url(request)
    assert url_one == JSON_API_PREFIX + f'{request}?'

    filters = {'route': 77, 'direction': 0}
    fields = ['name', 'stop_id']
    url_two = build_json_request_url(request, filters, fields)
    assert url_two == JSON_API_PREFIX + f'{request}?' + \
                        'filter[route]=77&' + \
                        'filter[direction]=0&' + \
                        'fields[route]=name,stop_id'

    url_three = build_json_request_url(request, filters)
    assert url_three == JSON_API_PREFIX + f'{request}?' + \
                        'filter[route]=77&' + \
                        'filter[direction]=0&'


def test_add_filters():
    filter_dict = {'route': 86, 'direction': 1}
    url = add_filters('', filter_dict)
    assert url == 'filter[route]=86&filter[direction]=1&'

    url = add_filters('', {'route': '57'})
    assert url == 'filter[route]=57&'

    url = add_filters('', {})
    assert url == ''


def test_sec_to_clock_time():
    assert sec_to_clock_time(1) == '00:01'
    assert sec_to_clock_time(63) == '01:03'
    assert sec_to_clock_time(3724) == '01:02:04'
