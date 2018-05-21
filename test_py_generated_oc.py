#! /usr/bin/env python3
"""
        Trying the generated openconfig-bgp.yang into
        python library

"""

from __future__ import print_function, unicode_literals
import xmltodict
import json
from ncclient import manager, xml_
from cisco_sandboxes import n9kv_netconf
import openconfig_bgp

if __name__ == '__main__':
    oc_bgp = openconfig_bgp.openconfig_bgp()
    oc_bgp.bgp.global_.config.as_ = 100
    oc_bgp.bgp.global_.config.router_id = '123.123.123.12'
    print(oc_bgp.get())

    xmlString = xmltodict.unparse(oc_bgp.get(), pretty=True)

    host = n9kv_netconf['address']
    port = n9kv_netconf['port']
    username = n9kv_netconf['username']
    password = n9kv_netconf['password']
    device_params = {'name': 'nexus'}

    with manager.connect(host=host, port=port, username=username,
                         password=password, hostkey_verify=False,
                         device_params=device_params,
                         look_for_keys=False, allow_agent=False) as m:
        try:
            success = m.edit_config(xmlString, target='running')
            print(success)
        except xml_.XMLError as xmlerr:
            print('Well, the generated library doesnt really help to generate netconf-ready xml..')
