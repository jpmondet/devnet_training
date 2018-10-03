#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Distributed under terms of the MIT license.
"""
Trying batfish
"""
from pybatfish.client.commands import *
from pybatfish.question.question import load_questions, list_questions
from pybatfish.question import bfq
from pybatfish.datamodel.flow import HeaderConstraints as header




bf_session.coordinatorHost = "172.17.0.2"
bf_session.coordinatorPort = "8888"
bf_session.apiKey = "061161f30fdd2d299733513fc17a8c2a6f1a4230f4332617"

load_questions(from_server=False)

#bf_init_snapshot(notebooks, name='candidate')
#bf_set_snapshot('candidate')

#ip_owners_ans = bfq.ipOwners().answer()

#ip_owners_ans.frame()

#iface_ans = bfq.interfaceProperties(nodes='as1border1', interfaces='GigabitEthernet0/0', properties='all-prefixes').answer()

#iface_ans.frame()
