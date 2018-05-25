#! /usr/bin/env python

"""
    Some practicing on the APIC Rest API
"""

from __future__ import print_function, unicode_literals
import requests
import json
from cisco_sandboxes import apicdc


AUTH_DATA = {
    "aaaUser": {
        "attributes": {
            "name": apicdc['username'],
            "pwd": apicdc['password']
        }
    }
}

TOKEN = ''


def get_token(json_data):
    """
        Parse a response to a auth post and update the global token
    """

    global TOKEN #pylint: disable=global-statement
    TOKEN = json_data['imdata'][0]['aaaLogin']['attributes']['token']

def auth_and_refresh(payload):
    """
        Authenticate and refresh when needed
    """

    url = apicdc['address']
    resp = requests.post(url + '/api/aaaLogin.json', data=json.dumps(payload), verify=False)
    try:
        get_token(json.loads(resp.text))
    except:
        print("Oops, issue getting token")
        raise

if __name__ == '__main__':
    """
     Main function
    """

    requests.packages.urllib3.disable_warnings() #pylint: disable=no-member

    auth_and_refresh(AUTH_DATA)
    print(TOKEN)
