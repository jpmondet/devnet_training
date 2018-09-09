#! /usr/bin/env python3
"""
    Simply get the OS version from a device 
"""

from nornir.core import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result

def main():
    nr = InitNornir(config_file="config.yaml")
    nx_host = nr.filter(site='earth', role='spine')
    version = nx_host.run(task=netmiko_send_command, command_string='sh version')
    
    print_result(version)
    


if __name__ == '__main__':
    main()
