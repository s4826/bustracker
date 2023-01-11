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

