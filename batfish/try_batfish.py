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

bf_init_snapshot("./candidate", name='candidate')
bf_set_snapshot('candidate')
print(bf_list_networks())

# Check AAA auth
print("#"*100)
print("Return nodes that do not require authentication on all lines.")
print("#"*100)
print(bfq.aaaAuthenticationLogin().answer().frame())

# Bgp peer config
print("#"*100)
print("Return BGP peer configuration properties.")
print("#"*100)
bgp_peer = bfq.bgpPeerConfiguration(nodes='as1border1')
print(bgp_peer.answer().frame())

# Bgp process config
print("#"*100)
print("Return BGP process configuration properties.")
print("#"*100)
bgp_proc = bfq.bgpProcessConfiguration(nodes='as1border1')
print(bgp_proc.answer().frame())

# Bgp Session compatibility
print("#"*100)
print("Return the status of configured BGP sessions, independent of remote peer configurations.")
print("#"*100)
bgp_sess_comp = bfq.bgpSessionCompatibility(nodes='as1border1', remoteNodes='as2border1')
print(bgp_sess_comp.answer().frame())

# Bgp Session status
print("#"*100)
print("Return the status of configured BGP sessions.")
print("#"*100)
bgp_sess_status = bfq.bgpSessionCompatibility(nodes='as1border1', remoteNodes='as2border1')
print(bgp_sess_status.answer().frame())

# Defined Structures
print("#"*100)
print("Lists the structures defined in the network, along with the files and line numbers in which they are defined.")
print("#"*100)
print(bfq.definedStructures().answer().frame())

# Detect Loops ! (looks like the loop I added intentionally was not detected :| )
print("#"*100)
print("Detect forwarding loops.")
print("#"*100)
print(bfq.detectLoops().answer().frame())

# Differential Reachability
#print("#"*100)
#print("Finds flows that are accepted in one snapshot but dropped in another.")
#print("#"*100)
#print(bfq.differentialReachability().answer().frame())

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

# Unreachable lines in ACL
print("#"*100)
print("Identify ACLs/filters with unreachable lines.")
print("#"*100)
print(bfq.filterLineReachability().answer().frame())

# Filter table (to filter the output of another question)
print("#"*100)
print("Return subset of answer for a question.")
print("#"*100)
print(bfq.filterTable(innerQuestion=bgp_peer).answer().frame())

# IF MTU
print("#"*100)
print("Find interfaces where the configured MTU matches the specified comparator and mtuBytes.")
print("#"*100)
print(bfq.interfaceMtu(mtuBytes=1450).answer().frame())

# IP Interfaces
#ip_owners_ans = bfq.ipOwners().answer()
#print(ip_owners_ans.frame())

# 1 specific interface
#iface_ans = bfq.interfaceProperties(nodes='as1border1', interfaces='GigabitEthernet0/0', properties='all-prefixes').answer()
#print(iface_ans.frame())


# Bgp properties
#print((bfq.bgpProperties(nodes='as1border1').answer()).frame()) #bgpProperties not working anymore ? 

# Bgp session
#print((bfq.bgpSessionStatus(nodes='as1border1').answer()).frame())


# Traceroute !!
#print((bfq.traceroute(startLocation='host1', headers={"dstIps": "ofLocation(host2)"}).answer()).frame())

