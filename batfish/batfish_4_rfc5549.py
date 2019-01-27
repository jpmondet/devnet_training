#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Distributed under terms of the MIT license.
# pylint: disable=no-member
"""
Trying batfish
"""
from pybatfish.client.commands import *
from pybatfish.client.session import Session
from pybatfish.question.question import load_questions, list_questions
from pybatfish.question import bfq
from pybatfish.datamodel.flow import HeaderConstraints as header
import logging

logger = logging.getLogger(__name__)

#bf_session = Session(logger)
#bf_session.coordinatorHost = "172.17.0.2"
#bf_session.coordinatorPort = "8888"
#bf_session.apiKey = ""
load_questions()

bf_init_snapshot("./5549", name='5549')
bf_set_snapshot('5549')
print(bf_list_networks())

# Bgp peer config
print("#"*100)
print("Return BGP peer configuration properties.")
print("#"*100)
bgp_peer = bfq.bgpPeerConfiguration(nodes='arista')
print(bgp_peer.answer().frame())
bgp_peer = bfq.bgpPeerConfiguration(nodes='n9k')
print(bgp_peer.answer().frame())

# Bgp process config
print("#"*100)
print("Return BGP process configuration properties.")
print("#"*100)
bgp_proc = bfq.bgpProcessConfiguration(nodes='arista')
print(bgp_proc.answer().frame())
bgp_proc = bfq.bgpProcessConfiguration(nodes='n9k')
print(bgp_proc.answer().frame())

# Bgp Session compatibility
print("#"*100)
print("Return the status of configured BGP sessions, independent of remote peer configurations.")
print("#"*100)
bgp_sess_comp = bfq.bgpSessionCompatibility(nodes='arista', remoteNodes='n9k')
print(bgp_sess_comp.answer().frame())
bgp_sess_comp = bfq.bgpSessionCompatibility(nodes='n9k', remoteNodes='arista')
print(bgp_sess_comp.answer().frame())

# Bgp Session status
print("#"*100)
print("Return the status of configured BGP sessions.")
print("#"*100)
bgp_sess_status = bfq.bgpSessionCompatibility(nodes='arista', remoteNodes='n9k')
print(bgp_sess_status.answer().frame())
bgp_sess_status = bfq.bgpSessionCompatibility(nodes='n9k', remoteNodes='arista')
print(bgp_sess_status.answer().frame())

# Bgp session
print("#"*100)
print("Another way to return bgp session status")
print("#"*100)
print((bfq.bgpSessionStatus(nodes='arista').answer()).frame())

# Defined Structures
print("#"*100)
print("Lists the structures defined in the network, along with the files and line numbers in which they are defined.")
print("#"*100)
print(bfq.definedStructures().answer().frame())

# Detect Loops 
print("#"*100)
print("Detect forwarding loops.")
print("#"*100)
print(bfq.detectLoops().answer().frame())

# List edges types
print("#"*100)
print("Lists neighbor relationships of the specified type (layer3, BGP, ospf, etc. in the form of edges).")
print("#"*100)
print(bfq.edges().answer().frame())

# File parse status
print("#"*100)
print("For each file in a snapshot, returns the host(s) that were produced by the file and the parse status: pass, fail, partially parsed.")
print("#"*100)
print(bfq.fileParseStatus().answer().frame())

# IP Interfaces
print("#"*100)
print("List IPs configured on interfaces")
print("#"*100)
ip_owners_ans = bfq.ipOwners().answer()
print(ip_owners_ans.frame())

# Traceroute !!
print("#"*100)
print("Traceroute ! The killer feature :-p")
print("#"*100)
print((bfq.traceroute(startLocation='arista', headers={"dstIps": "ofLocation(n9k)"}).answer()).frame())
print((bfq.traceroute(startLocation='n9k', headers={"dstIps": "ofLocation(arista)"}).answer()).frame())
#print((bfq.traceroute(startLocation='arista', headers={"dstIps": "ofLocation(arista)"}).answer()).frame())
