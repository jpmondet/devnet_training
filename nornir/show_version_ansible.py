#! /usr/bin/env python3
"""
    Simply get the OS version from a device 
"""

import ipdb
from pprint import pprint
import json

from nornir import InitNornir
from nornir.plugins.tasks import networking
from nornir.plugins.functions.text import print_result

def get_data(task):
    # task.host["vlans"] =
    data = task.run(
        task=networking.netmiko_send_command,
        command_string="show vlan",
        use_textfsm=True,
    )
    #task.host["vlans"] = process_data(data, config)
    print(data)
    print_result(data)

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

    #for host in nr.inventory.hosts.values():
    #    print(host)

    #facts = nr.run(task=networking.napalm_get, getters=["facts"])
    #print_result(facts)
    #intfs = nr.run(task=networking.napalm_get, getters=["config", "interfaces"])
    #print_result(intfs)

    #datas = nr.run(task=get_data)

    #version = nr.run(task=networking.napalm_cli, commands=['sh vlan | json'])

    #for name, data in version.items():
    #    for vlan in data.result.values():
    #        dict_vlan = json.loads(vlan)
    #        for vlan_infos in dict_vlan["TABLE_vlanbrief"]["ROW_vlanbrief"]:
    #            print(vlan_infos["vlanshowbr-vlanid"])

    #        #pprint(vlan["TABLE_vlanbrief"]["ROW_vlanbrief"][0])
    #        #pprint(vlan[0]["TABLE_vlanbrief"])

    version = nr.run(task=networking.napalm_cli, commands=['sh version'])
    print_result(version)
    #vlans = nr.run(task=networking.netmiko_send_command, command_string='sh vlan')#, use_textfsm=True)

    #print_result(vlans)

if __name__ == '__main__':
    main()
