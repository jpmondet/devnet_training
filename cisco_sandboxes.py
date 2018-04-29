#! /usr/bin/env python

# DevNet Always-On NETCONF/YANG & RESTCONF Sandbox Device
# https://devnetsandbox.cisco.com/RM/Diagram/Index/27d9747a-db48-4565-8d44-df318fce37ad?diagramType=Topology
iosxe_netconf = {
             "address": "ios-xe-mgmt.cisco.com",
             "port": 10000,
             "username": "root",
             "password": "D_Vay!_10&"
          }

iosxe_restconf = {
             "address": "ios-xe-mgmt.cisco.com",
             "port": 9443,
             "username": "root",
             "password": "D_Vay!_10&"
          }

# DevNet Always-On Sandbox APIC-EM
# https://devnetsandbox.cisco.com/RM/Diagram/Index/2e0f9525-5f46-4f46-973e-0f0c1bf934fa?diagramType=Topology
apicem = {
             "host": "sandboxapicem.cisco.com",
             "username": "devnetuser",
             "password": "Cisco123!",
             "port": 443
         }

# DevNet Always-On Sandbox ACI APIC
# https://devnetsandbox.cisco.com/RM/Diagram/Index/5a229a7c-95d5-4cfd-a651-5ee9bc1b30e2?diagramType=Topology
apicdc = {
             "host": "https://sandboxapicdc.cisco.com",
             "username": "admin",
             "password": "ciscopsdt",
             "port": 443
         }