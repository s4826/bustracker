# utils.py

from constants import JSON_API_PREFIX

def build_json_request_url(request_type, filter_dict=None, fields=None):
    url = JSON_API_PREFIX + request_type + "?"

    if filter_dict is not None:
        url = add_filters(url, filter_dict)

    if fields is not None:
        field_filter = ",".join(fields)
        url += f'fields[{request_type[:-1]}]=' + field_filter
    return url

def add_filters(url, filter_dict):

    # add sorting option if present
    if 'sort' in filter_dict:
        url += "sort={}&".format(filter_dict['sort'])

    for key in filter_dict:
        if 'sort' != key:
            url += "filter[{}]={}&".format(key, filter_dict[key])
    return url


def clock_time_difference(t1, t2):
    return sec_to_clock_time(abs(t1 - t2))


def sec_to_clock_time(seconds):
    h = seconds // 3600
    m = (seconds - h*3600) // 60
    s = (seconds - h*3600 - m*60)
    return f'{m:02}:{s:02}' if h== 0 \
            else f'{h:02}:{m:02}:{s:02}'


