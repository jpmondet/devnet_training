#! /usr/bin/env python3

"""
Some Rest/Restconf testings on IOS XE

"""

from pprint import pprint
import urllib3
import requests

from cisco_sandboxes import iosxe_restconf

#Constants
URIS_TO_TEST = [
    '.well-known/host-meta',
    'restconf/data/netconf-state/capabilities',
    'restconf/data/ietf-interfaces:interfaces',
    'restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2',
    'restconf/data/ietf-interfaces:interfaces/interface=Port-channel2',
    'restconf/data/ietf-interfaces:interfaces/interface/GigabitEthernet2?depth=1',
    'restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2/ipv4/address',
    'restconf/data/ietf-interfaces:interfaces-state/interface=GigabitEthernet2',
    'restconf/data/ietf-yang-library:modules-state',
    'restconf/data/ietf-restconf-monitoring:restconf-state/capabilities',
    'restconf/data/Cisco-IOS-XE-native:native/hostname',
    'restconf/data/Cisco-IOS-XE-native:native/interface',
    'restconf/operations/cisco-ia:save-config'
]

DATA = '''
{ "Cisco-IOS-XE-native:Port-channel":
		[
			{ 
                      "name": "2",
			  "description": "This is a port-channel interface",
			  "delay": 22222, 
			  "load-interval": 30, 
			  "mtu": 1501
			}
		]
}'''


def get_api_url(uri):
    """
     Formats the REST Get request and launch it.
    """

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}

    url = "https://{host}:{port}/{uri}".format(host=iosxe_restconf['address'],
                                               port=iosxe_restconf['port'], uri=uri)
    resp = requests.get(url,
                        auth=(iosxe_restconf['username'], iosxe_restconf['password']),
                        verify=False,
                        headers=headers
                       )
    return resp

def test_multiple_gets(uris):
    """
     Launches Get requests on multiple URIs.
    """

    for uri in uris:
        print('='*10 + ' Try uri : {uri} '.format(uri=uri) + '='*10)
        resp = get_api_url(uri)
        print(resp)
        try:
            pprint(resp.json())
        except Exception as e:
            print(resp.text)


def post_api_url(uri, data):
    """
     Formats the REST Post request and launch it.
    """

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}

    url = "https://{host}:{port}/{uri}".format(host=iosxe_restconf['address'],
                                               port=iosxe_restconf['port'], uri=uri)
    resp = requests.post(url,
                         auth=(iosxe_restconf['username'], iosxe_restconf['password']),
                         verify=False,
                         headers=headers,
                         data=data
                        )
    return resp

if __name__ == '__main__':
    """
        Main function using the functions defined before to actually use the APIs
    """



    test_multiple_gets(URIS_TO_TEST)

    response = post_api_url(URIS_TO_TEST[11], DATA)

    print(response)
    print(response.text)

    response = get_api_url(URIS_TO_TEST[4])
    print(response)
    print(response.text)
