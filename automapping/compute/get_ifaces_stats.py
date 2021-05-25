#!/usr/bin/python3

""" Get Interfaces stats from devices found while scrapping with lldp """

#TODO : Maybe get via snmp to increase chances to be multi-vendor ? 

from shutil import copyfile
from os import getenv
from itertools import groupby
from typing import Dict, List, Set, Any, Tuple
from ast import literal_eval
from json import dump, load
import time
import logging
import logging.config
from collections import OrderedDict, defaultdict
from base64 import b64decode
from ruamel import yaml as ryaml
from dotenv import load_dotenv
from ttp import ttp
from storage.db_layer import (
    bulk_update_collection,
    add_iface_stats,
    STATS_COLLECTION,
    UTILIZATION_COLLECTION
)
from nornir import InitNornir
from nornir.core import Nornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result

from draw_topology import drawing_advanced

load_dotenv()

def dump_results_to_db(device_name, ifaces_infos) -> None:
    #ifaces_list: List[Tuple[Dict[str, str], Dict[str,str]]] = []
    utilization_list: List[Tuple[Dict[str, str], Dict[str,str]]] = []
    stats_list: List[[Dict[str, str], Dict[str,str]]] = []
    for iface in ifaces_infos:
        iface_name = "/".join("".join(x) for is_number, x in groupby(iface["iface"], key=str.isdigit) if is_number is True)
        iface_stats_dict = {"device_name": device_name, "iface_name": iface_name, "timestamp": int(time.time())}
        iface_stats_dict.update(iface)
        stats_list.append(iface_stats_dict)
        # Each item of the lists are composed are the "query" (so the DB knows which entry to update
        # And the actual data
        query = {"device_name": device_name, "iface_name": iface_name}
        #update = {"speed": iface["bw"], "delay": iface["delay"], "mtu": iface["mtu"],
        #            "mac": iface["mac"], "bia_mac": iface["bia_mac"]}

        #ifaces_list.append((query, update))
        highest = int(iface["in_bytes"])
        lowest = int(iface["out_bytes"])
        if lowest > highest:
            highest = lowest
        utilization = {"device_name": device_name, "iface_name": iface_name, "last_utilization": highest}
        utilization_list.append((query, utilization))

    #bulk_update_collection(IFACES_COLLECTION, ifaces_list)
    bulk_update_collection(UTILIZATION_COLLECTION, utilization_list)
    add_iface_stats(stats_list)

def init_nornir_with_creds_and_scrap_infos() -> Nornir:

    # Update inventory with scrapped infos and credentials

    # TODO: Replace by DB infos
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

def collect_interfaces_stats(task):
    command = "show interface"
    task.host.open_connection("netmiko", configuration=task.nornir.config)
    result = task.run(
        task=netmiko_send_command, command_string=command
    )
    task.host.close_connection("netmiko")
    return result

def save_interfaces_stats(results):
    ifaces_stats = defaultdict(dict)
    with open("ifaces_stats.json") as ifaces_file:
        ifaces_stats.update(load(ifaces_file))

    for result in results:
        #print(result)
        #print(results[result][0])
        #print(results[result][0].result)
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
            dump_results_to_db(str(result), ifaces_infos)
                #ifaces_dict[iface["iface"]][int(time.time())] = iface 
            #ifaces_stats[result] = ifaces_dict
        except AttributeError as ae:
            print(f"[AttributeError] {ae}")
            print("Skipping the badly formated output of the device : {}".format(result))
            print("Bad formatted output : " + str(results[result][0].result))
            print("Bad formatted output : " + str(results[result][0].__dict__))
            ifaces_stats[result] = None
            continue
        except KeyError as ke:
            #print(f"[KeyError] {ke}, ifaces_stats[{result}] = {ifaces_stats[result]}")
            print(f"[KeyError] {ke}")
            #print(f"Ifaces weren't parsed correctly on device {result}")
            #print("Bad output : " + str(results[result][0].result[0]))
            ifaces_stats[result][iface["iface"]] = { int(time.time()) : iface }
            #print(f"[KeyError] {ke}, ifaces_stats[{result}] = {ifaces_stats[result]}")
            continue
        except TypeError as te:
            print(f"[TypeError] {te}, ifaces_stats[{result}] = {ifaces_stats[result]}")
            # Device was not created on ifaces_stats dict
            ifaces_stats[result] = { iface["iface"]: { int(time.time()) : iface } }
    
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

    while True:
        nr = init_nornir_with_creds_and_scrap_infos()

        logger.info("Getting iface stats details")
        start = time.time()

        get_ifaces_stats(nr)

        end = time.time()
        logger.info("TOTAL RUNTIME %s", str(round(end - start, 1)))

        time.sleep(60)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    main()
