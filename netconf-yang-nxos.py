#!/usr/bin/env python
""" 
	Trying netconf/yang on NX-OS
"""

import sys
from lxml import etree
from ncclient import manager
from cisco_sandboxes import n9kv_netconf



def find_in_response(xml, xmlns, to_find):
    """
        Trying to find a pattern in the xml response
    """
    found = ""
    found =  xml.find(".//{}{}".format(xmlns, to_find)).text
    return found

def get_nc(manager, filter='', xmlns='', target=''):
    """
        Get netconf from the device data and return a string 
    """

    resp = manager.get(('subtree', filter))
    response = resp.data
    if target:
        found = find_in_response(response, xmlns, target)
        return found
    response = etree.tostring(response, pretty_print=True)
    return response

def main():
    """
    Main method to connect to devices
    """

    get_oc_bgp = """
<bgp xmlns="http://openconfig.net/yang/bgp">
    <global>
        <state/>
    </global>
</bgp>
    """   

    host = n9kv_netconf['address']
    port = n9kv_netconf['port']
    username = n9kv_netconf['username']
    password = n9kv_netconf['password']
    device_params = {'name': 'nexus'}

    with manager.connect(host=host, port=port, username=username,
                         password=password, hostkey_verify=False,
                         device_params=device_params,
                         look_for_keys=False, allow_agent=False) as m:

        # print all NETCONF capabilities
        for capability in m.server_capabilities:
            print(capability.split('?')[0])

        # Collect the NETCONF response
        as_number = get_nc(m, get_oc_bgp, "{http://openconfig.net/yang/bgp}", "as")
        router_id = get_nc(m, get_oc_bgp, "{http://openconfig.net/yang/bgp}", "router-id")
        print("\nBGP AS: {} & router id : {}".format(as_number, router_id))

#        # Update the running config
#        netconf_response = m.edit_config(target='running', config=new_name)
#        # Parse the XML response
#        print("Response by the device after changing the name : ")
#        print(netconf_response)
#
#        new_ip = add_ip_interface.format(LOOPBACK_IP[device]['loopback'], LOOPBACK_IP[device]['ip'])
#        netconf_response = m.edit_config(target='running', config=new_ip)
#        # Parse the XML response
#        print("Response by the device after adding an interface & IP : ")
#        print(netconf_response)
#
#        # Get BGP ASN
#        netconf_response = m.get(('subtree', asn_filter))
#        # Parse the XML and print the data
#        xml_data = netconf_response.data_ele
#        asn = xml_data.find(".//{http://cisco.com/ns/yang/cisco-nx-os-device}asn").text
#        print("The ASN number for {} {} is {}".format(DEVICE_NAMES[device], device, asn))
#
#        # Get BGP RTRID
#        netconf_response = m.get(('subtree', bgp_rtrid_filter))
#        # Parse the XML response and print the data
#        xml_data = netconf_response.data_ele
#        rtrid = xml_data.find(".//{http://cisco.com/ns/yang/cisco-nx-os-device}rtrId").text
#        print("The BGP router-id for {} {} is {}".format(DEVICE_NAMES[device], device, rtrid))
#
#        # Add the prefix to BGP
#        print("\nNow adding prefix {} to device {} {}..\n".format(PREFIX[device], DEVICE_NAMES[device], device))
#        new_prefix = add_prefix.format(PREFIX[device])
#        netconf_response = m.edit_config(target='running', config=new_prefix)
#        # Parse the XML response
#        print(netconf_response)
#
#        # Add the loopback interface IP using OpenConfig model instead of Yang
#        print("\nNow adding IP address {} to interface {} on device {} {}...\n".format(IP_INT[device]['ip'],
#                                                                                       IP_INT[device]['name'], DEVICE_NAMES[device], device))
#        new_intf = add_oc_interface.format(IP_INT[device]['loopback'], IP_INT[device]['ip'])
#        netconf_response = m.edit_config(target='running', config=new_intf)
#        # Parse the XML response
#        print(netconf_response)
#
#        # Get bgp config with OpenConfig
#        netconf_response = m.get(('subtree', get_oc_bgp))
#        # Parse the XML response
#        xml_data = netconf_response.data_ele
#        asn = xml_data.find(".//{http://openconfig.net/yang/bgp}as").text
#
#        router_id = xml_data.find(".//{http://openconfig.net/yang/bgp}router-id").text
#
#        print("ASN number:{}, Router ID: {} for {} {}".format(asn, router_id, DEVICE_NAMES[device], device))



if __name__ == '__main__':
    sys.exit(main())

