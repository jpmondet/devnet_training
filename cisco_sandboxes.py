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
             "address": "sandboxapicem.cisco.com",
             "port": 443,
             "username": "devnetuser",
             "password": "Cisco123!"
         }

# DevNet Always-On Sandbox ACI APIC
# https://devnetsandbox.cisco.com/RM/Diagram/Index/5a229a7c-95d5-4cfd-a651-5ee9bc1b30e2?diagramType=Topology
apicdc = {
             "address": "https://sandboxapicdc.cisco.com",
             "port": 443,
             "username": "admin",
             "password": "ciscopsdt"
         }

# DevNet Always-On Sandbox N9kv !
# https://devnetsandbox.cisco.com/RM/Diagram/Index/dae38dd8-e8ee-4d7c-a21c-6036bed7a804?diagramType=Topology
n9kv_ssh = {
             "address": "sbx-nxos-mgmt.cisco.com",
             "port": 8181,
             "username": "admin",
             "password": "Admin_1234!"
         }

n9kv_nxapi = {
             "address": "http://sbx-nxos-mgmt.cisco.com",
             "port": 80,
             "username": "admin",
             "password": "Admin_1234!"
         }

n9kv_nxapi_s = {
             "address": "http://sbx-nxos-mgmt.cisco.com",
             "port": 443,
             "username": "admin",
             "password": "Admin_1234!"
         }

n9kv_restconf = {
             "address": "sbx-nxos-mgmt.cisco.com",
             "port": 443,
             "username": "admin",
             "password": "Admin_1234!"
         }

n9kv_netconf = {
             "address": "sbx-nxos-mgmt.cisco.com",
             "port": 10000,
             "username": "admin",
             "password": "Admin_1234!"
         }
