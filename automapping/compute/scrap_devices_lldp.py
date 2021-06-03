#!/usr/bin/python3

""" Scrapping topology infos by leveraging LLDP recursively """

from shutil import copyfile
from os import getenv
from typing import Dict, List, Set, Any, Tuple

# from ast import literal_eval
import time
import logging
import logging.config
from collections import OrderedDict
from itertools import groupby
from base64 import b64decode
from ruamel import yaml as ryaml
from dotenv import load_dotenv
from ttp import ttp
from storage.db_layer import (
    bulk_update_collection,
    NODES_COLLECTION,
    LINKS_COLLECTION,
)
from pymongo.errors import InvalidOperation
from nornir import InitNornir
from nornir.core import Nornir
from nornir.plugins.tasks.networking import netmiko_send_command

# from nornir.plugins.functions.text import print_result

# from dddraw_topology import drawing_advanced

load_dotenv()

SCRAPPED_DEVICES: Dict[str, str] = {}
SCRAPPED_DEVICES_BAD_FORMAT: Set = set()
FORMATTED_RESULTS: Dict = {}


def update_creds(nornir) -> None:

    for _, host in nornir.inventory.hosts.items():
        host.username = b64decode(getenv("USR_SW")).strip()
        host.password = b64decode(getenv("PWD_SW")).strip()


def dump_results_to_db() -> None:
    nodes_list: List[Tuple[Dict[str, str], Dict[str,str]]] = []
    #ifaces_list: List[Tuple[Dict[str, str], Dict[str,str]]] = []
    links_list: List[Tuple[Dict[str, str], Dict[str,str]]] = []
    for device_name, neighs_infos in FORMATTED_RESULTS.items():
        # Each item of the lists are composed are the "query" (so the DB knows which entry to update
        # And the actual data
        dev_name = device_name.lower()
        query = {"device_name": dev_name}

        # We add the device if it doesn't exist
        nodes_list.append((query, query))

        for neigh_infos in neighs_infos:
            neigh_name = neigh_infos["neighbor"].lower()
            query_neigh = {"device_name": neigh_name}
            # Stripping "Et, Ethernet, E,... " which can be different per equipment
            dev_iface = "/".join("".join(x) for is_number, x in groupby(neigh_infos["local_interface"], key=str.isdigit) if is_number is True)
            neigh_iface = "/".join("".join(x) for is_number, x in groupby(neigh_infos["neighbor_interface"], key=str.isdigit) if is_number is True)
            # We add its neigh if it doesn't exist
            nodes_list.append((query_neigh, query_neigh))

            #ifaces_list.append((query,
            #    {"iface_name": dev_iface, "device_name": dev_name}
            #))
            #ifaces_list.append((query_neigh,
            #    {
            #        "iface_name": neigh_iface,
            #        "device_name": neigh_name,
            #        "mac": neigh_infos["mac"],
            #    }
            #))
            links_list.append((query,
                {
                    "device_name": dev_name,
                    "iface_name": dev_iface,
                    "neighbor_name": neigh_name,
                    "neighbor_iface": neigh_iface,
                }
            ))
            links_list.append((query_neigh,
                {
                    "device_name": neigh_name,
                    "iface_name": neigh_iface,
                    "neighbor_name": dev_name,
                    "neighbor_iface": dev_iface,
                }
            ))

    try:
        bulk_update_collection(NODES_COLLECTION, nodes_list)
        bulk_update_collection(LINKS_COLLECTION, links_list)
    except InvalidOperation:
        print("Nothing to dump to db (wasn't able to scrap devices?), passing..")


def format_neighbor_to_inventory(neighbor):

    host_infos = OrderedDict()

    # The return of LLDP command is different on different types of devices
    # I modified ntc_template to avoid this difference in Returned structure
    # and stay standard
    neigh_key = "neighbor"

    host_infos["hostname"] = neighbor[neigh_key].lower()

    # Placeholer to correct some weirdly formatted names
    if host_infos["hostname"] == "weirdly-formatted-name":
        host_infos["hostname"] = "better-name"

    if "iou" in host_infos["hostname"]:
        host_infos["hostname"] = neighbor["mgmt_address"]

    # Find nei_type depending on its system description:
    try:
        if (
            "cisco" in neighbor["system_description"].lower()
            or "IOS" in neighbor["system_description"]
        ):
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
                    # ttp used for regexin'
                    # A lil' slow tho..
                    tplate_text = tplate.read()
                    parser = ttp(result[key][0].result.result, tplate_text)
                    parser.parse()
                    neighs_infos = parser.result()[0][0]["neighs"]
                    if not isinstance(neighs_infos, list):
                        neighs_infos = [neighs_infos]
                    FORMATTED_RESULTS[key] = neighs_infos
            # print("Adding {} to graph".format(key))
            except AttributeError as atterr:
                print(f"[AttributeError] {atterr}")
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
                if neigh_name == "weird-name":
                    neigh_name = "better-name"
                nei["neighbor"] = neigh_name

                # Prevent scrapping again devices that were already scrapped
                # (via another link for example)
                if neigh_name not in SCRAPPED_DEVICES:
                    # Placeholder to limit scrapping to interesting devices
                    # (could be needed if, for example, servers decide to use lldp)
                    if "sw" in neigh_name or "rtr" in neigh_name:
                        neigh_infos = format_neighbor_to_inventory(nei)
                        hosts_yaml[neigh_name] = neigh_infos
            except TypeError as terr:
                print(f"[TypeError]: {terr}")
                print(
                    "[TypeError] Skipping the badly formated NEIGHBOR of the device : {}".format(
                        key
                    )
                )
                print("Bad formatted nei : " + str(nei))
            except KeyError as keyerr:
                print(keyerr)
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
    task.host.open_connection("netmiko", configuration=task.nornir.config)
    result = task.run(
        task=netmiko_send_command, command_string=command
    )  # , use_textfsm=True, severity_level=logging.DEBUG)
    task.host.close_connection("netmiko")
    return result


def recursive_scrapping(nornir, inventory):

    # No more devices to scrap, stopping the recursion
    if len(nornir.inventory.hosts) < 1:  # pylint: disable=len-as-condition
        return

    # Scrapping lldp infos
    result = nornir.run(task=collect_neighbors)

    # Updating the inventory for subsequent runs
    update_scrapping_dicts_and_inventory(result, nornir)

    # Initiate or continue the Recursion
    # nornir = InitNornir(core={"num_workers": 10}, inventory=inventory)
    with open("hosts.yaml") as hyaml:
        print(hyaml.read())
    nornir = InitNornir(
        core={"num_workers": 4}, inventory=inventory, ssh={"config_file": "./iou.ssh"}
    )
    update_creds(nornir)
    recursive_scrapping(nornir, inventory)


def main() -> None:
    """Prepare nornir's inventory, start the recursion
    and then compile the results.

    EXTRA CARE: NTC_TEMPLATES WERE MODIFIED to make lldp
    work correctly everywhere"""

    # environ['NET_TEXTFSM'] = '~/ntc-templates/templates'

    # Copying the start inventory file into the file that will be scrapped and overwritten
    # 'hosts_start' contains the first 1 or 2 hosts to start with
    while True:
        copyfile("hosts_start.yaml", "hosts.yaml")

        # Peparing nornir's inventory
        # (could be better to retrieve infos from SoT)
        inventory: Dict[str, Any] = {
            "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
            "options": {"host_file": "hosts.yaml", "group_file": "groups.yaml"},
        }
        nornir = InitNornir(inventory=inventory, ssh={"config_file": "./iou.ssh"})
        update_creds(nornir)

        logger.info("Getting neigh details")
        start = time.time()

        # This step is here to retrieve some cached data that
        # were saved in a file on a previous run (when we don't
        # want to scrap all devices again, which can be long on
        # large topos
        # global FORMATTED_RESULTS
        # with open("graph_ct", "r") as res:
        #    FORMATTED_RESULTS = literal_eval(res.read())
        # for key in FORMATTED_RESULTS.keys():
        #    SCRAPPED_DEVICES[key] = ""

        # We start scrapping :
        recursive_scrapping(nornir, inventory)
        end = time.time()
        logger.info("COMMANDS RUN IN %s", str(round(end - start, 1)))

        ########################################
        # Infos retrieved are saved into files
        # with open("graph_ct", "w") as res:
        #    res.write(str(FORMATTED_RESULTS))
        # with open("failed_devices", "w") as failed:
        #    failed.write(str(SCRAPPED_DEVICES_BAD_FORMAT))
        # with open("scrapped_devices", "w") as succeed:
        #    succeed.write(str(SCRAPPED_DEVICES))
        #########################################
        # Dump to DB instead of files :
        dump_results_to_db()
        time.sleep(300)

    # Draw a graph from the infos retrieved thanks to 'draw_topology' module
    # print("\n\nGenerating the Graph, please wait.\n\n")
    # drawing_advanced(FORMATTED_RESULTS)

    #end = time.time()
    #logger.info("TOTAL RUNTIME %s", str(round(end - start, 1)))


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    main()
