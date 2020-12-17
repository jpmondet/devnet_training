#!/usr/bin/python3

""" Scrapping topology infos by leveraging LLDP recursively """

from shutil import copyfile
from os import getenv
from typing import Dict, List, Set, Any
from ast import literal_eval
from json import dump, load
import time
import logging
import logging.config
from collections import OrderedDict, defaultdict
from base64 import b64decode
from ruamel import yaml as ryaml
from nornir import InitNornir
from nornir.core import Nornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from dotenv import load_dotenv
from ttp import ttp

from draw_topology import drawing_advanced

load_dotenv()

SCRAPPED_DEVICES: Dict[str, str] = {}
SCRAPPED_DEVICES_BAD_FORMAT: Set = set()
FORMATTED_RESULTS: Dict = {}

def init_nornir_with_creds_and_scrap_infos() -> Nornir:

    # Update inventory with scrapped infos and credentials

    scrapped: Dict[str, str] = {}
    with open("scrapped_devices") as sdf:
        scrapped = literal_eval(sdf.read())

    hosts_nr: Dict[Dict[str, str]] = OrderedDict()
    for host, hostname in scrapped.items():
        host_infos: Dict[str, str] = OrderedDict()
        host_infos["hostname"] = hostname
        # Find nei_type depending on its system description:
        if "iou" in host:
            nei_type = "cisco_ios"
        else:
            nei_type = "whatever"

        host_infos["groups"] = [nei_type]

        hosts_nr[host] = host_infos

    with open("hosts.yaml", "w") as hosts:
        #dump(hosts_nr, hosts)
        ryaml.round_trip_dump(hosts_nr, hosts)

    # Now that hosts.yaml file is ready, with start Nornir
    inventory: Dict[str, Any] = {
        "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
        "options": {"host_file": "hosts.yaml", "group_file": "groups.yaml"},
    }
    nornir = InitNornir(core={"num_workers": 4}, inventory=inventory, ssh={'config_file': './iou.ssh'})

    # Update creds with env vars
    for _, host in nornir.inventory.hosts.items():
        host.username = b64decode(getenv("USR_SW")).strip()
        host.password = b64decode(getenv("PWD_SW")).strip()

    return nornir


def update_scrapping_dicts_and_inventory(result, nornir: Nornir):

    hosts_yaml = OrderedDict()

    for key in result:
        # Nice debug prints xD
        # print(result)
        # print(result[key])
        # print(result[key][0])
        # print(result[key][0].result)
        # print(result[key][0].result.result)
        # print(result[key][0].result.result[0])
        if not FORMATTED_RESULTS.get(key):
            try:
                with open("lldp.tplate") as tplate:
                    tplate_text = tplate.read()
                    parser = ttp(result[key][0].result.result, tplate_text)
                    parser.parse()
                    neighs_infos = parser.result()[0][0]["neighs"]
                    if not isinstance(neighs_infos, list):
                        neighs_infos = [neighs_infos]
                    FORMATTED_RESULTS[key] = neighs_infos
            # print("Adding {} to graph".format(key))
            except AttributeError as ae:
                print(f"[AttributeError] {ae}")
                print("Skipping the badly formated output of the device : {}".format(key))
                print("Bad formatted output : " + str(result[key][0].result))
                SCRAPPED_DEVICES[key] = nornir.inventory.hosts[key].hostname
                SCRAPPED_DEVICES_BAD_FORMAT.add(key)
                continue

        SCRAPPED_DEVICES[key] = nornir.inventory.hosts[key].hostname
        for nei in FORMATTED_RESULTS[key]:
            try:
                # Placeholder if lil' fixes must be made to devices names
                # (can be needed to handle snowflake topologies)

                neigh_name = nei["neighbor"].lower()
                if neigh_name == 'weird-name':
                    neigh_name = 'better-name'
                nei["neighbor"] = neigh_name


                # Prevent scrapping again devices that were already scrapped
                # (via another link for example)
                if not neigh_name in SCRAPPED_DEVICES:
                    # Placeholder to limit scrapping to interesting devices
                    # (could be needed if, for example, servers decide to use lldp)
                    if 'sw' in neigh_name or 'rtr' in neigh_name:
                        neigh_infos = format_neighbor_to_inventory(nei)
                        hosts_yaml[neigh_name] = neigh_infos
            except TypeError as te:
                print(f"[TypeError]: {te}")
                print(
                    "[TypeError] Skipping the badly formated NEIGHBOR of the device : {}".format(
                        key
                    )
                )
                print("Bad formatted nei : " + str(nei))
            except KeyError as ke:
                print(ke)
                print(
                    "[KeyError] Skipping the badly formated NEIGHBOR of the device : {}".format(key)
                )
                print("Bad formatted nei : " + str(nei))

    print(hosts_yaml)
    # print(SCRAPPED_DEVICES)
    with open("hosts.yaml", "w") as hosts:
        ryaml.round_trip_dump(hosts_yaml, hosts)


def collect_interfaces_stats(task):
    command = "show interface"
    result = task.run(
        task=netmiko_send_command, command_string=command
    )
    return result

def save_interfaces_stats(results):
    ifaces_stats = defaultdict(dict)
    with open("ifaces_stats.json") as ifaces_file:
        ifaces_stats.update(load(ifaces_file))

    for result in results:
        if "rtr" in result:
            with open("interface_rtr.tplate") as tplate:
                tplate_text = tplate.read()
        else:
            with open("interface_sw.tplate") as tplate:
                tplate_text = tplate.read()
        try:
            parser = ttp(results[result][0].result.result, tplate_text)
            parser.parse()
            ifaces_infos = parser.result()[0][0]["ifaces"]
            if not isinstance(ifaces_infos, list):
                ifaces_infos = [ifaces_infos]

            # Transform list as dict (will be easier to access each attrbute when drawing graph)
            # Also add a timestamp
            #ifaces_dict: Dict[str, Dict[str, Any]] = ifaces_stats[result]
            for iface in ifaces_infos:
                ifaces_stats[result][iface["iface"]][int(time.time())] = iface
                #ifaces_dict[iface["iface"]][int(time.time())] = iface 
            #ifaces_stats[result] = ifaces_dict
        except AttributeError as ae:
            print(f"[AttributeError] {ae}")
            print("Skipping the badly formated output of the device : {}".format(result))
            print("Bad formatted output : " + str(results[result][0].result))
            ifaces_stats[result] = None
            continue
        except KeyError as ke:
            print(f"[KeyError] {ke}")
            print(f"Ifaces weren't parsed correctly on device {result}")
            print("Bad output : " + str(results[result][0].result[0]))
            ifaces_stats[result] = None
            continue
    
    with open("ifaces_stats.json", "w") as ifaces_file:
        dump(ifaces_stats, ifaces_file)



def get_ifaces_stats(nornir):

    # Scrapping interfaces infos
    results = nornir.run(task=collect_interfaces_stats)
    save_interfaces_stats(results)

def main() -> None :
    """ Prepare nornir's inventory with scrapped
        infos from previous runs (when building graph)
    """

    nr = init_nornir_with_creds_and_scrap_infos()

    logger.info("Getting neigh details")
    start = time.time()

    get_ifaces_stats(nr)
    end = time.time()
    logger.info("COMMANDS RUN IN %s", str(round(end - start, 1)))

    ## Infos retrieved are saved into files
    #with open("graph_ct", "w") as res:
    #    res.write(str(FORMATTED_RESULTS))
    #with open("failed_devices", "w") as failed:
    #    failed.write(str(SCRAPPED_DEVICES_BAD_FORMAT))
    #with open("scrapped_devices", "w") as succeed:
    #    succeed.write(str(SCRAPPED_DEVICES))

    ## Draw a graph from the infos retrieved thanks to 'draw_topology' module
    #print("\n\nGenerating the Graph, please wait.\n\n")
    #drawing_advanced(FORMATTED_RESULTS)

    end = time.time()
    logger.info("TOTAL RUNTIME %s", str(round(end - start, 1)))


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    main()
