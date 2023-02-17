"""Utility methods"""

from .constants import JSON_API_PREFIX


def build_json_request_url(endpoint, filter_dict=None, fields=None):
    """
    Build an MBTA v3 API request url, including an optional dictionary
    of filters and fields to limit the response size.

    :param endpoint: Base name of a v3 API endpoint (i.e. "stops", "routes").
        All allowed values can be found at
        "https://api-v3.mbta.com/docs/swagger/index.html".
    :param filter_dict: Dictionary of result element/value combinations
        for result filtering (e.g. {"route": "77", "direction": 0})
    :param fields: Fields to include for each matching record. Specifying
        only the fields you need can help limit response size.
    """
    url = JSON_API_PREFIX + endpoint + "?"

    if filter_dict is not None:
        url = add_filters(url, filter_dict)

    if fields is not None:
        field_filter = ",".join(fields)
        url += f"fields[{endpoint[:-1]}]=" + field_filter
    return url


def add_filters(url, filter_dict):
    """
    Add filters from a dictionary to a base url in the format
    '{URL}?filter[key1]=value1&filter[key2]=value2...'

    :param url: Base URL
    :param filter_dict: Dictionary of filter names/values
    """
    # add sorting option if present
    if "sort" in filter_dict:
        url += f'sort={filter_dict["sort"]}&'

    for key in filter_dict:
        if "sort" != key:
            url += f"filter[{key}]={filter_dict[key]}&"
    return url


def generate_confirmation_email_content(token):
    """Generate confirmation email content based on a confirmation token"""

    link = f"http://localhost:5000/confirm_account/{token}"
    content = (
        "Thanks for registering with the bustracker app!\n"
        + "Please confirm your email address at the following link.\n\n"
        + f"{link}"
    )

    return content
