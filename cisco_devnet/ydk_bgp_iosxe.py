#!/usr/bin/env python3

from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.openconfig import openconfig_bgp as oc_bgp
#from ydk.errors import YPYModelError

from cisco_sandboxes import iosxe_netconf

#The provider is the underlying implementation that connects to the device
iosxe_provider = NetconfServiceProvider(address=iosxe_netconf['address'], \
                                     port=iosxe_netconf['port'], \
                                     username=iosxe_netconf['username'], \
                                     password=iosxe_netconf['password'], \
                                     protocol='ssh')

#CRUDSerice provides the CRUD functions
crud_service = CRUDService()

#Configuration entity for BGP
bgp_config = oc_bgp.Bgp()

#Read and print the initial value
initial_bgp = crud_service.read(iosxe_provider, bgp_config)
print("The initial BGP ASN value is - " + str(initial_bgp.global_.config.as_))

#Set a new value
if initial_bgp.global_.config.as_:
    #Delete the configuration entity so that we can create a new one
    crud_service.delete(iosxe_provider, bgp_config)
    bgp_config.global_.config.as_ = int(initial_bgp.global_.config.as_) - 1
else:
    bgp_config.global_.config.as_ = 65000 
#Create the configuration
crud_service.create(iosxe_provider, bgp_config)

#Read and print the new value
new_bgp = crud_service.read(iosxe_provider, bgp_config)
print("The new BGP ASN value is - " + str(new_bgp.global_.config.as_))

if initial_bgp.global_.config.as_:
    #Reset to initial value
    crud_service.delete(iosxe_provider, bgp_config)
    bgp_config.global_.config.as_ = int(initial_bgp.global_.config.as_)
    crud_service.create(iosxe_provider, bgp_config)
    #Read and print the value now that we have reset it
    initial_bgp = crud_service.read(iosxe_provider, bgp_config)
    print("The BGP ASN value is now - " + str(initial_bgp.global_.config.as_))

#Try and set to invalid value
bgp_config.global_.config.as_ = -1
try:
    crud_service.create(iosxe_provider, bgp_config)
except Exception as e:
    print("Setting the ASN to -1 didn't work, as expected - " + str(e))
