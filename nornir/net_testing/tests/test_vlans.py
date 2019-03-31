#! /usr/bin/env python3

from operator import itemgetter
from pathlib import Path
from typing import Dict, Any

import json
from ruamel.yaml import YAML
from nornir.plugins.tasks import networking
# from nornir.core.filter import F


CONFIG_FILE = "vlans_to_validate.yaml"


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
    reslt = task.run(task=networking.napalm_cli, commands=['sh vlan | json']).result
    vlans = parse_vlan_ids_nxos(reslt)
    task.host['vlans'] = vlans


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
        assert configured_vlans == desired_vlans, f"Failed for host: {host.name} : configured vlans = {configured_vlans} vs desired vlans = {desired_vlans}"
