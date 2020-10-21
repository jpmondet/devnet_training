#!/usr/bin/env python
""" 
	Trying netconf/yang on NX-OS
"""

import sys
from lxml import etree, builder
import xml.dom.minidom
#import xmltodict
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

def config_bgp_openconfig(nc_manager):
    """
        Trying to configure a whole bgp config with openconfig models
    """
    config_bgp = """
<config>
    <bgp xmlns="http://openconfig.net/yang/bgp">
        <global>
            <config>
                <as>100</as>
                <router-id>100.100.100.100</router-id>
            </config>
            <use-multiple-paths>
            </use-multiple-paths>
        </global>
        <peer-groups>
            <peer-group peer-group-name='eBGP_peer'>
                <config>
                    <peer-group-name>eBGP_peer</peer-group-name>
                </config>
            </peer-group>
        </peer-groups>
        <neighbors>
            <neighbor>
                <config>
                    <description>Configured_by_netconfig_based_on_openconfig_yang</description>
                    <peer-as>1234</peer-as>
                    <local-as>5678</local-as>
                    <neighbor-address>1.2.3.4</neighbor-address>
                    <peer-group>eBGP_peer</peer-group>
                    <send-community>BOTH</send-community>
                </config>
                <ebgp-multihop>
                    <config>
                        <multihop-ttl>10</multihop-ttl>
                    </config>
                </ebgp-multihop>
                <logging-options>
                    <config>
                        <log-neighbor-state-changes>true</log-neighbor-state-changes>
                    </config>
                </logging-options>
                <route-reflector>
                    <config>
                        <route-reflector-cluster-id>1234</route-reflector-cluster-id>
                    </config>
                </route-reflector>
                <timers>
                    <config>
                        <hold-time>30</hold-time>
                        <keepalive-interval>10</keepalive-interval>
                        <minimum-advertisement-interval>0</minimum-advertisement-interval>
                        <connect-retry>35</connect-retry>
                    </config>
                </timers>
                <transport>
                    <config>
                        <passive-mode>true</passive-mode>
                    </config>
                </transport>
                <neighbor-address>1.2.3.4</neighbor-address>
            </neighbor>
        </neighbors>
    </bgp>
</config>
    """

    # Could use lxml builder to prepare the config in a lil' more programatic way
    # Example : 
    elem_maker = builder.ElementMaker()
    elem_maker_ns = builder.ElementMaker(namespace='http://openconfig.net/yang/bgp')
    bgp_elem = elem_maker_ns.bgp
    config_elem = elem_maker.config(bgp_elem)
    etree.tostring(config_elem)

    success = nc_manager.edit_config(config_bgp, target='running')
    print(success)




def main():
    """
    Main method to connect to devices
    """
    #<global>
    #    <config/>
    #</global>

    get_oc_bgp = """
<bgp xmlns="http://openconfig.net/yang/bgp">
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
        #for capability in m.server_capabilities:
        #    print(capability.split('?')[0])

        # Collect the NETCONF response
       # as_number = get_nc(m, get_oc_bgp, "{http://openconfig.net/yang/bgp}", "as")
       # router_id = get_nc(m, get_oc_bgp, "{http://openconfig.net/yang/bgp}", "router-id")
       # print("\nBGP AS: {} & router id : {}".format(as_number, router_id))

        config_bgp_openconfig(m)
        # Get all config
        resp = m.get_config('running', ('subtree',get_oc_bgp))
        pretty_config = xml.dom.minidom.parseString(resp.xml).toprettyxml()
        print(pretty_config)
        
        #with open('running_nxos.cfg', 'w+') as cfg_file:
        #    cfg_file.write(pretty_config)

        #with open('running_nxos.xml', 'w+') as xml_file:
        #    xml_file.write(resp.xml)


        #resp_dict = xmltodict.parse(resp.xml)["rpc-reply"]["data"]

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

