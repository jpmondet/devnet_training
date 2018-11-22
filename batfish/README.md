# Testing Batfish with python Client

## Batfish server

docker run -p 9997:9997 -p 9996:9996 batfish/batfish

## Snapshots

Snapshots must be structured in a specific way.

Example of structure :

**Candidate directory**
  - **configs subdirectory** (network devices)
       - R1_candidate.cfg
       - R2_candidate.cfg
       - ....
  - **hosts subdirectory** (servers)
       - host1.json 
       - host2.json
       - ....
  - **iptables** (optional for servers)
       - host1.iptables
       - host2.iptables
       - ....
  - **topology subdirectory** (also optional on a Routed topology cause Batfish can deduce from the interfaces IPs)

Hosts & topology files are in ``json`` format.

Iptables files can be dumped with ``iptables-save`` command.

## Batfish Client

Via the client (here python script), we can check facts about the snapshoted topology by asking "Questions".

List of questions already developed : https://pybatfish.readthedocs.io/en/latest/questions.html#module-pybatfish.question.bfq


## Ansible modules

`batfish_init`
`batfish_policy`
`batfish_searchfilters`

