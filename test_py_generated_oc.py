#! /usr/bin/env python3
"""
        Trying the generated openconfig-bgp.yang into
        python library

"""

from __future__ import print_function, unicode_literals
import xmltodict
import json
from ncclient import manager, xml_
from cisco_sandboxes import iosxe_restconf
import openconfig_bgp
import requests
import urllib3
requests.packages.urllib3.disable_warnings()

def get_api_url(uri):
    """
     Formats the REST Get request and launch it.
    """

    # Preparing the content & url
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http_auth = requests.auth.HTTPBasicAuth(iosxe_restconf['username'], iosxe_restconf['password'])
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}
    url = "https://{host}:{port}/{uri}".format(host=iosxe_restconf['address'],
                                               port=iosxe_restconf['port'], uri=uri)
    # Actual Get request is thrown
    print('Sending get request on url : {}'.format(url))
    resp = requests.get(url,
                        auth=http_auth,
                        verify=False,
                        headers=headers
                       )
    return resp

def post_api_url(uri, data):
    """
     Formats the REST Post request and launch it.
    """

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}
    headers = {'Content-Type': 'application/yang-data+json'}

    http_auth = requests.auth.HTTPBasicAuth(iosxe_restconf['username'], iosxe_restconf['password'])
    url = "https://{host}:{port}/{uri}".format(host=iosxe_restconf['address'],
                                               port=iosxe_restconf['port'], uri=uri)
    print('Sending post request on url : {} with data: {}'.format(url, data))
    resp = requests.post(url,
                         auth=http_auth,
                         verify=False,
                         headers=headers,
                         data=data
                        )
    return resp


if __name__ == '__main__':
    oc_bgp = openconfig_bgp.openconfig_bgp()
    oc_bgp.bgp.global_.config.as_ = 100
    oc_bgp.bgp.global_.config.router_id = '123.123.123.12'
    print(oc_bgp, type(oc_bgp))
    print(json.dumps(oc_bgp.get()['bgp']['global']['config']))

    # resp = post_api_url('restconf/data/openconfig-bgp:bgp/',json.dumps(oc_bgp.get()['bgp']['global']['config']))
    # print(resp, resp.text)


    # resp = get_api_url('restconf/data/openconfig-interfaces:interfaces/')
    resp = get_api_url('restconf/data/openconfig-bgp:bgp/?depth=unbounded')
    # resp = get_api_url('restconf/data/openconfig-bgp-policy:bgp-policy/?depth=unbounded')
    # resp = get_api_url('/restconf/data/restconf-state/capabilities')
    # resp = get_api_url('/restconf/data?fields=ietf-yang-library:modules-state/module(name;revision;schema;namespace)')
    # resp = get_api_url('restconf/data/')
    print(resp, resp.text)
