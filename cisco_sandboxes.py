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

# Devnet always-on DNA Center
# https://devnetsandbox.cisco.com/RM/Diagram/Index/471eb739-323e-4805-b2a6-d0ec813dc8fc?diagramType=Topology
dnac = {
             "address": "https://sandboxdnac2.cisco.com",
             "port": 443,
             "username": "devnetuser",
             "password": "Cisco123!"
        }

# Devnet always-on IOS-XR box
# https://devnetsandbox.cisco.com/RM/Diagram/Index/e83cfd31-ade3-4e15-91d6-3118b867a0dd?diagramType=Topology
iosxr_ssh = {
             "address": "sbx-iosxr-mgmt.cisco.com",
             "port": 8181,
             "username": "admin",
             "password": "C1sco12345"
        }

iosxr_netconf = {
             "address": "sbx-iosxr-mgmt.cisco.com",
             "port": 10000,
             "username": "admin",
             "password": "C1sco12345"
        }

iosxr_bash = {
             "address": "sbx-iosxr-mgmt.cisco.com",
             "port": 8282,
             "username": "admin",
             "password": "C1sco12345"
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

# Trex sandbox : https://devnetsandbox.cisco.com/RM/Diagram/Index/2ec5952d-8bc5-4096-b327-c294acd9512d?diagramType=Topology
# Istio sandbox : https://devnetsandbox.cisco.com/RM/Diagram/Index/8b9512a7-d2e5-4699-8d7a-393d7434982f?diagramType=Topology
