#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Distributed under terms of the MIT license.
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
#bf_session.apiKey = "6887facfc39dd574a914327eb31fd04427f25f4cbea6fb97"
load_questions()

bf_init_snapshot("./candidate", name='candidate')
bf_set_snapshot('candidate')

# IP Interfaces
ip_owners_ans = bfq.ipOwners().answer()
print(ip_owners_ans.frame())

# 1 specific interface
iface_ans = bfq.interfaceProperties(nodes='as1border1', interfaces='GigabitEthernet0/0', properties='all-prefixes').answer()
print(iface_ans.frame())

# Bgp peer config -> On Docs but looks like it's not implemented
#bgp_peer = bfq.bgpPeerConfiguration(nodes='as1border1')
#print(bgp_peer.frame())

# Bgp properties
print((bfq.bgpProperties(nodes='as1border1').answer()).frame())

# Bgp session
print((bfq.bgpSessionStatus(nodes='as1border1').answer()).frame())


# Traceroute !!
print((bfq.traceroute(startLocation='host1', headers={"dstIps": "ofLocation(host2)"}).answer()).frame())

