# devnet_training
Some network-oriented developments using APIs/Netconf/Yang/etc. (self-trainings, nothing fancy)

# Some reminders/cheatsheets

## Yang

``pyang --tree-help``

``pyang -f tree <yang_module>``

``pyang -f tree --tree-path path/to/target <yang_module>``

``pyang -f tree --tree-depth 2 <yang_module>``

**Getting Netconf ready formats :** (the output might need some corrections though)
``pyang -f sample-xml-skeleton --sample-xml-skeleton-path path/to/target <yang_module>``

``pyang -f sample-xml-skeleton --sample-xml-skeleton-path path/to/target --sample-xml-skeleton-doctype=config  <yang_module>``


**Validating modules :**
``pyang --lint <yang_module>``

**Generating python :**
``export PYBINDPLUGIN=`/usr/bin/env python -c 'import pyangbind; import os; print("%s/plugin" % os.path.dirname(pyangbind.__file__))'``
``pyang -p /path/to/target --plugindir $PYBINDPLUGIN -f pybind openconfig-bgp.yang > openconfig-bgp.py``


## Nornir automation

``nornir.core.InitNornir`` -> function to init with conf/code

Example config file : 
```
num_workers: 100
inventory: nornir.plugins.inventory.simple.SimpleInventory
SimpleInventory:
    host_file: "inventory/hosts.yaml"
    group_file: "inventory/groups.yaml"
```
Example hosts inventory :
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
