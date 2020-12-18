#!/usr/bin/python3

""" Scrapping topology infos by leveraging LLDP recursively """

from shutil import copyfile
from os import getenv
from typing import Dict, List, Set, Any
from ast import literal_eval
import time
import logging
import logging.config
from collections import OrderedDict
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

def update_creds(nornir):

    for _, host in nornir.inventory.hosts.items():
        host.username = b64decode(getenv("USR_SW")).strip()
        host.password = b64decode(getenv("PWD_SW")).strip()


def format_neighbor_to_inventory(neighbor):

    host_infos = OrderedDict()

    # The return of LLDP command is different on different types of devices
    # I modified ntc_template to avoid this difference in Returned structure
    # and stay standard
    neigh_key = "neighbor"

    host_infos["hostname"] = neighbor[neigh_key].lower()

    # Placeholer to correct some weirdly formatted names
    if host_infos["hostname"] == 'weirdly-formatted-name':
        host_infos["hostname"] = 'better-name'

    if "iou" in host_infos["hostname"]:
        host_infos["hostname"] = neighbor["mgmt_address"]

    # Find nei_type depending on its system description:
    try:
        if "cisco" in neighbor["system_description"].lower() or "IOS" in neighbor["system_description"]:
            nei_type = "cisco_ios"
    except KeyError:
        nei_type = "cisco_ios"

    host_infos["groups"] = [nei_type]

    return host_infos


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


def collect_neighbors(task):
    command = "show lldp neigh detail"
    result = task.run(
        task=netmiko_send_command, command_string=command
        ) #, use_textfsm=True, severity_level=logging.DEBUG)
    return result


def collect_transceivers_infos(task):
    command = "show interface transceiver detail"
    result = task.run(
        task=netmiko_send_command, command_string=command, severity_level=logging.DEBUG
    )
    return result

def recursive_scrapping(nornir, inventory):

    # No more devices to scrap, stopping the recursion
    if len(nornir.inventory.hosts) < 1:  # pylint: disable=len-as-condition
        return

    # Scrapping lldp infos
    result = nornir.run(task=collect_neighbors)

    # Scrapping interfaces infos
    #result = nornir.run(task=collect_interfaces_stats)
    #process_interfaces_stats_to_crc(result)

    # Updating the inventory for subsequent runs
    update_scrapping_dicts_and_inventory(result, nornir)

    # Initiate or continue the Recursion
    #nornir = InitNornir(core={"num_workers": 10}, inventory=inventory)
    with open("hosts.yaml") as hy:
        print(hy.read())
    nornir = InitNornir(core={"num_workers": 4}, inventory=inventory, ssh={'config_file': './iou.ssh'})
    update_creds(nornir)
    recursive_scrapping(nornir, inventory)


def main() -> None :
    """ Prepare nornir's inventory, start the recursion
    and then compile the results.

    EXTRA CARE: NTC_TEMPLATES WERE MODIFIED to make lldp 
    work correctly everywhere """

    # environ['NET_TEXTFSM'] = '~/ntc-templates/templates'

    # Copying the start inventory file into the file that will be scrapped and overwritten
    # 'hosts_start' contains the first 1 or 2 hosts to start with
    copyfile("hosts_start.yaml", "hosts.yaml")

    # Peparing nornir's inventory
    inventory: Dict[str, Any] = {
        "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
        "options": {"host_file": "hosts.yaml", "group_file": "groups.yaml"},
    }
    nr = InitNornir(inventory=inventory,ssh={"config_file":"./iou.ssh"})
    update_creds(nr)

    logger.info("Getting neigh details")
    start = time.time()

    # This step is here to retrieve some cached data that 
    # were saved in a file on a previous run (when we don't
    # want to scrap all devices again, which can be long on 
    # large topos
    global FORMATTED_RESULTS
    with open("graph_ct", "r") as res:
        FORMATTED_RESULTS = literal_eval(res.read())
    for key in FORMATTED_RESULTS.keys():
        SCRAPPED_DEVICES[key] = ""

    # We start scrapping :
    recursive_scrapping(nr, inventory)
    end = time.time()
    logger.info("COMMANDS RUN IN %s", str(round(end - start, 1)))

    # Infos retrieved are saved into files
    with open("graph_ct", "w") as res:
        res.write(str(FORMATTED_RESULTS))
    with open("failed_devices", "w") as failed:
        failed.write(str(SCRAPPED_DEVICES_BAD_FORMAT))
    with open("scrapped_devices", "w") as succeed:
        succeed.write(str(SCRAPPED_DEVICES))

    # Draw a graph from the infos retrieved thanks to 'draw_topology' module
    print("\n\nGenerating the Graph, please wait.\n\n")
    drawing_advanced(FORMATTED_RESULTS)

    end = time.time()
    logger.info("TOTAL RUNTIME %s", str(round(end - start, 1)))


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    main()
