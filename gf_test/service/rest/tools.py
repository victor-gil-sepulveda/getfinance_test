import os

import requests

from gf_test.service.rest.restmethod import RestMethod

API_PREFIX = "gftest"


def ep_url(server_address, endpoint, version):
    url = os.path.join(server_address, API_PREFIX, version, endpoint)
    return url


def do_request(endpoint_address, method, data=None):
    if method == RestMethod.GET:
        response = requests.get(endpoint_address)
        try:
            val = response.json()
        except ValueError:
            val = {}
        return val

    elif method == RestMethod.POST:
        response = requests.post(endpoint_address, json=data)
        try:
            val = response.json()
        except ValueError:
            val = {}
        return val


