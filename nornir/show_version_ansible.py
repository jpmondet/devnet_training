#! /usr/bin/env python3
"""
    Simply get the OS version from a device 
"""

import ipdb
from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result

def main():
    #nr = InitNornir(config_file="config.yaml")
    nr = InitNornir(
        core={"num_workers": 5},
        inventory={
            "plugin": "nornir.plugins.inventory.ansible.AnsibleInventory",
            "options": {
                "hostsfile": "hosts"
            }
        }
    )

    #print(nr.inventory.hosts)
   
    #facts = nr.run(task=networking.napalm_get, getters=["facts"])
    #print_result(facts)

    version = nr.run(task=networking.napalm_cli, commands=['sh version'])

    print_result(version)


if __name__ == '__main__':
    main()
