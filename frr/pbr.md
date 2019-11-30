# Using PBRs

## Prequisites

In `/etc/frr/daemons`:  
`pbrd=yes`

## Exple config

pbr table range 15555 17777

nexthop-group NH1
 nexthop eth1
 nexthop eth2

pbr-map PBRMAP1 seq 10
 match src-ip 11.11.11.11/32
 match dst-ip 22.22.22.22/32
 set nexthop-group NH1

interface eth0
 pbr-policy PBRMAP1


## Under the hood

PBRs uses kernel `ip rules` and routes tables.

For each **nexthop-group**, a table will be created with a default route :

`ip route show table 15555`
```
default  proto 195  metric 20
	nexthop dev eth1 weight 1
	nexthop dev eth2 weight 1
```

Then when applying the **pbr-map** to the interface (via **pbr-policy**), it creates an `ip rule` entry that map the content of the pbr-map to the interface and to the table :

`ip rule`
```
0:	from all lookup local
309:	from 11.11.11.11 to 22.22.22.22 iif lo lookup 15555
32766:	from all lookup main
32767:	from all lookup default
```

The `rule` is placed before the `main` lookup so the pbr will be processed before and voila !
