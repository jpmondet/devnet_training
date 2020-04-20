#! /usr/bin/env python3

from operator import itemgetter
from pathlib import Path
from typing import Dict, Any

import json
from ruamel.yaml import YAML
from nornir import InitNornir
from nornir.plugins.tasks import networking

# from nornir.core.filter import F
from nornir.plugins.functions.text import print_result


CONFIG_FILE = "to_validate.yaml"


def load_config(config_file: str) -> Dict[str, Any]:
    yaml = YAML(typ="safe")
    dir_path = Path(__file__).parent
    with open(dir_path / config_file) as f:
        return yaml.load(f)


def parse_vlan_ids_nxos(reslt):
    parsed_result = []
    for vlan in reslt.values():
        dict_vlan = json.loads(vlan)
        for vlan_infos in dict_vlan["TABLE_vlanbrief"]["ROW_vlanbrief"]:
            name = vlan_infos["vlanshowbr-vlanname"]
            _id = vlan_infos["vlanshowbr-vlanid"]
            vlan_parsed = {"id": int(_id), "name": name}
            parsed_result.append(vlan_parsed)
    return sorted(parsed_result, key=itemgetter("id"))


def get_vlan_napalm(task, config):
    # Absolutely not vendor-dependent
    reslt = task.run(
        task=networking.napalm_cli, commands=["sh vlan | json"]
    ).result
    vlans = parse_vlan_ids_nxos(reslt)
    task.host["vlans"] = vlans


def process_data(data, config):
    result = []
    for vlan_data in data:
        name = vlan_data["name"]
        _id = int(vlan_data["vlan_id"])
        if _id not in config["excluded_vlans"]:
            vlan_dict = {"id": _id, "name": name}
            result.append(vlan_dict)
    return sorted(result, key=itemgetter("id"))


def get_data(task, config):
    # task.host["vlans"] =
    data = task.run(
        task=networking.netmiko_send_command,
        command_string="show vlan | json",
        use_textfsm=True,
    ).result
    task.host["vlans"] = process_data(data, config)


def test_vlans(nr):
    config = load_config(CONFIG_FILE)
    # hosts = nr.filter(F(groups__contains=config["group"]))
    nr.run(task=get_vlan_napalm, config=config)

    desired_vlans = config["data"]["vlans"]
    for host in nr.inventory.hosts.values():
        configured_vlans = host["vlans"]
        assert (
            configured_vlans == desired_vlans
        ), f"Failed for host: {host.name} : configured vlans = {configured_vlans} vs desired vlans = {desired_vlans}"


#def get_bgp_neigh_state(task):
#    """
#       Using napalm this time  
#    """
#
#    result = task.run(task=networking.napalm_get, getters=["get_bgp_neighbors"]).result
#    task.host["bgp_neigh_state"] = result
#
#
#def test_bgp_state(nr):
#    nr.run(task=get_bgp_neigh_state)
#
#    config = load_config(CONFIG_FILE)
#
#    # Testing that the desired neighbors are up
#    desired_bgp_neigh_ip = config["data"]["neigh"]["ip"]
#    desired_bgp_neigh_as = config["data"]["neigh"]["remote_as"]
#
#    for host in nr.inventory.hosts.values():
#        dict_bgp_neigh_state = json.loads(host["bgp_neigh_state"])
#    assert True


def get_bgp_config(task):
    """
        Unfortunately, had to use cli string (with netmiko)... Thanks nxos.
    """

    result = task.run(
        task=networking.netmiko_send_command,
        command_string="show run bgp | json",
    ).result
    task.host["bgp_config"] = result


def test_bgp_config(nr):
    # hosts = nr.filter(F(groups__contains=config["group"]))
    nr.run(task=get_bgp_config)

    config = load_config(CONFIG_FILE)

    # Testing that the right AS is configured
    desired_bgp_as = config["data"]["as"]
    desired_bgp_neighs = config["data"]["neighs"]
    desired_bgp_neigh_ip = config["data"]["neigh"]["ip"]
    desired_bgp_neigh_as = config["data"]["neigh"]["remote_as"]
    for host in nr.inventory.hosts.values():
        dict_bgp_config = json.loads(host["bgp_config"])
        configured_bgp_as = dict_bgp_config["nf:filter"]["m:configure"][
            "m:terminal"
        ]["router"]["bgp"]["__XML__PARAM__as"]["__XML__value"]
        assert (
            int(configured_bgp_as) == desired_bgp_as
        ), f"Failed for host: {host.name} : configured bgp as = {configured_bgp_as} \
vs desired bgp as = {desired_bgp_as}"

        neighbors_configured_list = dict_bgp_config["nf:filter"]["m:configure"][
            "m:terminal"
        ]["router"]["bgp"]["__XML__PARAM__as"]["m2:neighbor"]
        #print(type(neighbors_configured_list))
        #print(neighbors_configured_list)
        #print(isinstance(neighbors_configured_list, list))
        if not isinstance(neighbors_configured_list, list):
            configured_bgp_neigh_as = dict_bgp_config["nf:filter"][
                "m:configure"
            ]["m:terminal"]["router"]["bgp"]["__XML__PARAM__as"]["m2:neighbor"][
                "m2:__XML__PARAM__neighbor-id"
            ][
                "m4:remote-as"
            ][
                "m4:__XML__PARAM__asn"
            ][
                "m4:__XML__value"
            ]
            configured_bgp_neigh_ip = dict_bgp_config["nf:filter"][
                "m:configure"
            ]["m:terminal"]["router"]["bgp"]["__XML__PARAM__as"]["m2:neighbor"][
                "m2:__XML__PARAM__neighbor-id"
            ][
                "m2:__XML__value"
            ]
            assert (
                configured_bgp_neigh_ip == desired_bgp_neigh_ip
            ), f"Failed for host: {host.name} : configured bgp neigh ip = {configured_bgp_neigh_ip} \
    vs desired bgp neigh ip = {desired_bgp_neigh_ip}"
            assert (
                configured_bgp_neigh_ip in desired_bgp_neighs.keys()
            ), f"Failed for host: {host.name} : configured bgp neigh ip = {configured_bgp_neigh_ip} \
    vs desired bgp neigh ip = {desired_bgp_neigh_ip}"
            assert (
                int(configured_bgp_neigh_as) == desired_bgp_neighs["configured_bgp_neigh_ip"]
            ), f"Failed for host: {host.name} : configured bgp neigh as = {configured_bgp_neigh_as} \
    vs desired bgp neigh as = {desired_bgp_neigh_as}"
        else:
            # If there are multiple bgp neighbors configured, NXOS change de json schema.......

            # We build a simple dict with the configured values to mirror the one on our validation file
            # It will be easier to assert this way
            configured_bgp_neighs = {}
            for neighbor_configured in neighbors_configured_list:
                configured_bgp_neighs[
                    neighbor_configured["m2:__XML__PARAM__neighbor-id"][
                        "m2:__XML__value"
                    ]] = int(neighbor_configured["m2:__XML__PARAM__neighbor-id"]["m4:remote-as"]["m4:__XML__PARAM__asn"]["m4:__XML__value"])

            # We check is every desired neighbor is there (and that there isn't too much neighbors either)
            assert (
                desired_bgp_neighs == configured_bgp_neighs
            ), f"Failed for host: {host.name} : desired_bgp_neighs = {desired_bgp_neighs}, configured_bgp_neighs = {configured_bgp_neighs}"


def main():
    """
    napalm support for nxos :

    get_arp_table (nxos_ssh only)
    get_bgp_neighbors
    get_config
    get_environment
    get_facts
    get_interfaces
    get_interfaces_ip
    get_lldp_neighbors
    get_lldp_neighbors_detail
    get_mac_address_table
    get_network_instances (nxos nxapi only)
    get_ntp_peers
    get_ntp_servers
    get_ntp_stats (nxos nxapi only)
    get_route_to (nxos_ssh only)
    get_snmp_information
    get_users
    is_alive
    ping
    traceroute
    load_template
    """

    nr = InitNornir(
        core={"num_workers": 5},
        inventory={
            "plugin": "nornir.plugins.inventory.ansible.AnsibleInventory",
            "options": {"hostsfile": "hosts"},
        },
    )
    results = nr.run(task=networking.napalm_get, getters=["get_bgp_neighbors"])
    print_result(results)

    #print("#" * 15, "Starting BGP Config tests", "#" * 15)
    #test_bgp_config(nr)
    #print("#" * 15, "BGP Config tests Passed!", "#" * 15)


if __name__ == "__main__":
    main()

"""
sbx-ao# sh run bgp | json-pretty 
{
    "nf:source": {
        "nf:running": null
    }, 
    "nf:filter": {
        "m:configure": {
            "m:terminal": {
                "feature": {
                    "bgp": null
                }, 
                "router": {
                    "bgp": {
                        "__XML__PARAM__as": {
                            "__XML__value": "65535", 
                            "m1:router-id": {
                                "m1:__XML__PARAM__router-id": {
                                    "m1:__XML__value": "172.16.0.1"
                                }
                            }, 
                            "m1:timers": {
                                "m1:prefix-peer-timeout": {
                                    "m1:__XML__PARAM__prefixpeer-timeout": {
                                        "m1:__XML__value": "30"
                                    }
                                }
                            }, 
                            "m2:address-family": {
                                "m2:ipv4": {
                                    "m2:unicast": {
                                        "m3:network": {
                                            "m3:__XML__PARAM__ip-prefix": {
                                                "m3:__XML__value": "172.16.0.0/16"
                                            }
                                        }
                                    }
                                }
                            }, 
                            "m2:neighbor": {
                                "m2:__XML__PARAM__neighbor-id": {
                                    "m2:__XML__value": "172.16.0.2", 
                                    "m4:remote-as": {
                                        "m4:__XML__PARAM__asn": {
                                            "m4:__XML__value": "65535"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

"""
