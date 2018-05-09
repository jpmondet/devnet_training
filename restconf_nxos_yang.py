#! /usr/bin/env python3

"""
Some Rest/Restconf testings on NX-OS

"""

from pprint import pprint
import urllib3
import requests

from cisco_sandboxes import n9kv_restconf

#Constants
URIS_TO_TEST = [
    '.well-known/host-meta',
    'restconf/data/?fields=ietf-yang-library:modules-state/module',
    'restconf/data/?fields=ietf-yang-library:modules-state/module(name;revision;schema;namespace)',
    'restconf/data/netconf-state/capabilities',
    'restconf/data/retconf-state/capabilities',
    'restconf/data/ietf-restconf-monitoring:restconf-state/capabilities',
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
{
  "System": {
    "ipv4-items": {
      "inst-items": {
        "dom-items": {
          "Dom-list": [
            {
              "name": "default",
              "if-items": {
                "If-list": [
                  {
                    "id": "lo234",
                    "addr-items": {
                      "Addr-list": [
                        {
                          "addr": "1.2.3.4/32"
                        }
                      ]
                    }
                  }
                ]
              }
            }
          ]
        }
      }
    },
    "intf-items": {
      "lb-items": {
        "LbRtdIf-list": [
          {
            "adminSt": "up",
            "id": "lo234"
          }
        ]
      }
    }
  }
}'''


def get_api_url(uri):
    """
     Formats the REST Get request and launch it.
    """
    
    # Preparing the content & url
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http_auth = requests.auth.HTTPBasicAuth(n9kv_restconf['username'], n9kv_restconf['password'])
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}
    url = "https://{host}:{port}/{uri}".format(host=n9kv_restconf['address'],
                                               port=n9kv_restconf['port'], uri=uri)
    # Actual Get request is thrown
    resp = requests.get(url,
                        auth=http_auth,
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
    headers = {'Content-Type': 'application/yang-data+json'}

    url = "https://{host}:{port}/{uri}".format(host=n9kv_restconf['address'],
                                               port=n9kv_restconf['port'], uri=uri)
    resp = requests.post(url,
                         auth=(n9kv_restconf['username'], n9kv_restconf['password']),
                         verify=False,
                         headers=headers,
                         data=data
                        )
    return resp

if __name__ == '__main__':
    """
        Main function using the functions defined before to actually use the APIs
    """



    #test_multiple_gets(URIS_TO_TEST)

    #response = post_api_url(URIS_TO_TEST[11], DATA)
    #response = post_api_url('ins', DATA)

    #print(response)
    #print(response.text)

    #response = get_api_url(URIS_TO_TEST[1])
    #response = get_api_url('restconf/data/Cisco-NX-OS-device:System/bgp-items/inst-items/dom-items/Dom-list?content=config')
    response = get_api_url('restconf/data/openconfig-interfaces:interfaces/')
    
    print(response)
    print(response.text)
