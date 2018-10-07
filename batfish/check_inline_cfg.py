#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Distributed under terms of the MIT license.

"""

"""
from pybatfish.client.commands import *
from pybatfish.question.question import load_questions, list_questions
from pybatfish.question import bfq
from pybatfish.datamodel.flow import HeaderConstraints
import os
import tempfile


def create_inline_snapshot(text, format="cisco"):
    """ Create a quick inline snapshot """

    HOSTNAME = "TEST_INLINE"
    ACL_TEXT = """
    !RANCID-CONTENT-TYPE: {format}
    hostname {hostname}
    {text}
    """.format(format=format, hostname=HOSTNAME, text=text)
    temp = tempfile.TemporaryDirectory(prefix='bf_acl.')
    snap_dir = os.path.join(temp.name, 'configs')
    snap_filename = os.path.join(snap_dir, HOSTNAME)
    os.makedirs(snap_dir)
    with open(snap_filename, 'w') as outfile:
        outfile.write(ACL_TEXT)
    
    bf_set_network('__inline_snap')
    return bf_init_snapshot(temp.name)

if __name__ == "__main__":
    acl_def = """
    no ip access-list extended TEST_ACL
    ip access-list extended TEST_ACL
    10 permit tcp any any
    20 permit udp any any
    30 deny tcp any any eq ssh
    """

    load_questions()
    snap_gen = create_inline_snapshot(acl_def)
    print("#"*100)
    print("TEST ACL LINE REACHABILITY (here seq 30 should be useless and thus 'unreachable')")
    reacha = bfq.filterLineReachability().answer(snap_gen)
    print(reacha.frame())
    print("#"*100)
    print("CHECK IF ACL REALLY BLOCKS THE PACKET SPECIFIED")
    test_behav = bfq.searchfilters(
        action="permit", headers=HeaderConstraints(
            applications=["ssh"], srcIps="1.2.3.4", dstIps="4.5.6.7"
            )
        ).answer()
    print(test_behav)
    print("#"*100)
    print("DEFINES ON WHICH ENTRY THE PACKET SPECIFIED IS MATCHED")
    test_acl = bfq.testfilters(
        headers=HeaderConstraints(
            applications=["ssh"], srcIps="1.2.3.4", dstIps="4.5.6.7"
            )
        ).answer()
    print(test_acl)
