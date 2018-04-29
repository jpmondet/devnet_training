#! /usr/bin/env python3

"""
Some Rest/Restconf testings

"""

import requests
import urllib3
import json
from pprint import pprint

from cisco_sandboxes import iosxe_netconf
from cisco_sandboxes import iosxe_restconf
from cisco_sandboxes import apicem
from cisco_sandboxes import apicdc


def get_api_url(uri):

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}

    url = "https://{host}:{port}/{uri}".format(host=iosxe_restconf['address'], port=iosxe_restconf['port'], uri=uri)
    response = requests.get(url,
                            auth = (iosxe_restconf['username'], iosxe_restconf['password']),
                            verify = False,
                            headers = headers
                           )
    return response

if __name__ == '__main__':

    uris_to_test = [
                    '.well-known/host-meta', 
                    'restconf/data/netconf-state/capabilities', 
                    'restconf/data/ietf-interfaces:interfaces', 
                    'restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2', 
                    'restconf/data/ietf-interfaces:interfaces/interface=Port-channel1', 
                    'restconf/data/ietf-interfaces:interfaces/interface/GigabitEthernet2?depth=1', 
                    'restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2/ipv4/address', 
                    'restconf/data/ietf-interfaces:interfaces-state/interface=GigabitEthernet2', 
                    'restconf/data/ietf-yang-library:modules-state', 
                    'restconf/data/ietf-restconf-monitoring:restconf-state/capabilities', 
                    'restconf/data/Cisco-IOS-XE-native:native/hostname', 
                    'restconf/data/Cisco-IOS-XE-native:native/interface', 
                    'restconf/operations/cisco-ia:save-config'
                    ]

    for uri in uris_to_test:
        print('='*10 + ' Try uri : {uri} '.format(uri = uri) + '='*10)
        response = get_api_url(uri)
        print(response)
        try:
            pprint(response.json())
        except Exception as e:
            print(response.text)

    #headers = {'content-type': 'application/yang-data+json',
    #           'accept': 'application/yang-data+json, application/yang-data.errors+json'}
    data = '''
    { "Cisco-IOS-XE-native:Port-channel": 
    		[
    			{ "name": "2",
    			  "description": "This is a port-channel interface",
    			  "delay": 22222, 
    			  "load-interval": 30, 
    			  "mtu": 1501,
    			  "address": 
    			  	[
    			  		"ip": "1.1.1.1/24"
    			  	]
    			}
    		]
    }'''
    #print(json.dumps(data))
    #response = requests.post(url,
    #                        auth = (username, password),
    #                        data=data, headers=headers,
    #                        verify = False
    #                       )

    #print(response)
    #print(response.text)
