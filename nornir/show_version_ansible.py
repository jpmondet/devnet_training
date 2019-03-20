#! /usr/bin/env python3
"""
    Simply get the OS version from a device 
"""

from nornir.core import InitNornir
from nornir.plugins.tasks.networking import napalm_cli
from nornir.plugins.functions.text import print_result

def main():
    nr = InitNornir(config_file="config_ansible.yaml")
    print(nr.inventory.to_dict())
    nx_host = nr.filter(platform='nx-os')
    print(nx_host.to_dict())
    version = nx_host.run(task=napalm_cli, commands=['sh version'])
    
    print_result(version)
    


if __name__ == '__main__':
    main()
