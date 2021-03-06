# devnet_training
Some network-oriented developments using APIs/Netconf/Yang/etc. (self-trainings, nothing fancy)

# Some reminders/cheatsheets

## Yang

(Must be in the directory of the module or `--path` must be specified to indicate where to search dependencies of the module)

``pyang --tree-help``

``pyang -f tree <yang_module>``

``pyang -f tree --tree-path path/to/target <yang_module>``

``pyang -f tree --tree-depth 2 <yang_module>``

``pyang -f tree --tree-depth 10 bgp/openconfig-bgp.yang -p bgp -p rib -p policy -p types --tree-path bgp/neighbors/neighbor/afi-safis/afi-safi/ipv6-unicast``

`` --tree-print-groupings`` Also print from which file each dependencies of the module were taken.

(Interesting enough there is also an output as `-f jstree` to browse the output in a browser. Similarly YangExplorer allows browsing & generating RPC requests)

**Getting Netconf ready formats :** (the output might need some corrections though)
``pyang -f sample-xml-skeleton --sample-xml-skeleton-path path/to/target <yang_module>``

``pyang -f sample-xml-skeleton --sample-xml-skeleton-path path/to/target --sample-xml-skeleton-doctype=config  <yang_module>``


**Validating modules :**
``pyang --lint <yang_module>``

We can also validate modules via the website `yangvalidator.com`. This one is interesting since it can validate against a specific RFC and/or Draft.

**Generating python :**
``export PYBINDPLUGIN=`/usr/bin/env python -c 'import pyangbind; import os; print("%s/plugin" % os.path.dirname(pyangbind.__file__))'``
``pyang -p /path/to/target --plugindir $PYBINDPLUGIN -f pybind openconfig-bgp.yang > openconfig-bgp.py``

OR 

Use of ydk-gen to generate python (or other) libs from yang modules + a profile file (mostly metadatas) : 
``python generate.py --python --bundle profile_file.json``


## Nornir automation

### This was for nornir 1.x, nornir 2.x broke most of the things below (https://nornir.readthedocs.io/en/stable/upgrading/1_to_2.html)

``nornir.core.InitNornir`` -> function to init with conf/code

Example config file : 
```
---
num_workers: 100
inventory: nornir.plugins.inventory.simple.SimpleInventory
SimpleInventory:
    host_file: "inventory/hosts.yaml"
    group_file: "inventory/groups.yaml"
```
Example hosts inventory (can use an Ansible style inventory also)
```yaml
---
host1.earth:
    nornir_host: 1.2.3.4
    nornir_ssh_port: 22
    nornir_username: user
    nornir_password: pass
    site: earth
    role: spine
    groups:
        - earth
    nornir_nos: whateveros
    type: network_device
```
Example groups file : 
```yaml
---
defaults:
    domain: solar.space
solar:
    asn: 65100
earth:
    groups:
        - solar
```
Simple snippet : 
```python
from nornir.plugins.tasks import networking

earth_spine = nr.filter(site="earth", role="spine")
result = earth_spine.run(task=networking.napalm_get,
                        getters=["facts"])
print_result(result)
```
Tasks provided : https://nornir.readthedocs.io/en/latest/plugins/tasks/index.html
Simple custom task : 
```python
def list_hosts(task, random_arg):
    print(f"{task.host.name}, {random_arg}")

nr.run(task=list_hosts, num_workers=1, random_arg=1)
```

### Nornir 2.x


``nornir.InitNornir`` -> function to init with conf/code

Example config file : 
```
---
num_workers: 100
inventory: nornir.plugins.inventory.simple.SimpleInventory
SimpleInventory:
    host_file: "inventory/hosts.yaml"
    group_file: "inventory/groups.yaml"
```
Example hosts inventory (can use an Ansible style inventory also)
```yaml
---
host1.earth:
    hostname: 1.2.3.4
    port: 22
    username: user
    password: pass
    platform: whateveros
    groups:
      - earth
    data:
      site: earth
      role: spine
      type: network_device
```
Example groups file : 
```yaml
---
global:
  data:
    domain: solar.space
solar:
  data:
    asn: 65100
earth:
    groups:
        - solar
```
Simple snippet : 
```python
from nornir import InitNornir
from nornir.plugins.tasks import networking

nr = InitNornir(config_file="config.yaml") (or the config can be inline)
earth_spine = nr.filter(site="earth", role="spine")
result = earth_spine.run(task=networking.napalm_get,
                        getters=["facts", "interfaces"])
print_result(result)
```
Tasks provided : https://nornir.readthedocs.io/en/latest/plugins/tasks/index.html
Simple custom task : 
```python
def list_hosts(task, random_arg):
    print(f"{task.host.name}, {random_arg}")

nr.run(task=list_hosts, num_workers=1, random_arg=1)
```

### Leverage Ansible inventory

Not a lot to change :
1. Modify the config file to : 
```
inventory: nornir.plugins.inventory.ansible.AnsibleInventory
AnsibleInventory:
  hostsfile: "hosts"
```
2. Add the mandatory variables if you don't have them already (`platform`, `hostname`, `username`, `password`, `port`)
