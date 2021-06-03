#! /usr/bin/env python3

from os import getenv
import asyncio
from itertools import groupby
from binascii import hexlify
from time import time, sleep
from typing import List, Dict, Any, Tuple
from pymongo.errors import InvalidOperation
from pysnmp.error import PySnmpError
from dpath.util import search
from storage.db_layer import (
    prep_db_if_not_exist,
    bulk_update_collection,
    NODES_COLLECTION,
    LINKS_COLLECTION,
    get_all_nodes
)
from snmp_functions import get_table, get_snmp_v3_creds, NEEDED_MIBS_FOR_LLDP as NEEDED_MIBS

SNMP_USR = getenv("SNMP_USR")
SNMP_AUTH_PWD = getenv("SNMP_AUTH_PWD")
SNMP_PRIV_PWD = getenv("SNMP_PRIV_PWD")

def dump_results_to_db(device_name, lldp_infos) -> None:
    nodes_list: List[Tuple[Dict[str, str], Dict[str,str]]] = []
    links_list: List[Tuple[Dict[str, str], Dict[str,str]]] = []

    # Each item of the lists are composed by the "query" (so the DB knows which entry to update
    # And the actual data
    dev_name = device_name.lower()
    query = {"device_name": dev_name}
    # We add the device if it doesn't exist
    nodes_list.append((query, query))

    for lldp_nei in lldp_infos:
        # Getting neigh node infos and adding it to nodes_list
        _, neigh_name = next(search(lldp_nei, f"{NEEDED_MIBS['lldp_neigh_name']}*", yielded=True))
        if not neigh_name:
            continue
        neigh_name = neigh_name.lower()

        # IP is a lil' special since it is written in the oid (yeah weird)
        neigh_ip_oid, _ = next(search(lldp_nei, f"{NEEDED_MIBS['lldp_neigh_ip']}*", yielded=True))
        neigh_ip = '.'.join(neigh_ip_oid.split('.')[-4:])
        query_neigh = {"device_name": neigh_name}
        nodes_list.append((query_neigh, {"device_name": neigh_name, "device_ip": neigh_ip}))


        # Getting neigh and local ifaces infos and adding them to link list
        _, local_iface = next(search(lldp_nei, f"{NEEDED_MIBS['lldp_local_iface']}*", yielded=True))
        _, neigh_iface = next(search(lldp_nei, f"{NEEDED_MIBS['lldp_neigh_iface']}*", yielded=True))
        # Stripping "Et, Ethernet, E,... " which can be different per equipment
        dev_iface = "/".join("".join(x) for is_number, x in groupby(local_iface, key=str.isdigit) if is_number is True)
        neigh_iface = "/".join("".join(x) for is_number, x in groupby(neigh_iface, key=str.isdigit) if is_number is True)

        query_link = {
            "device_name": dev_name,
            "iface_name": dev_iface,
            "neighbor_name": neigh_name,
            "neighbor_iface": neigh_iface,
        }

        links_list.append((query_link, query_link))

        query_neigh_link = {
            "device_name": neigh_name,
            "iface_name": neigh_iface,
            "neighbor_name": dev_name,
            "neighbor_iface": dev_iface,
        }
        links_list.append((query_neigh_link, query_neigh_link))

    try:
        bulk_update_collection(NODES_COLLECTION, nodes_list)
        bulk_update_collection(LINKS_COLLECTION, links_list)
    except InvalidOperation:
        print("Nothing to dump to db (wasn't able to scrap devices?), passing..")

async def get_device_lldp_infos(target_name, oids, credentials, target_ip=None):
    
    target = target_ip if target_ip else target_name

    try:
        res = get_table(target, oids, credentials)
        dump_results_to_db(target_name, res)
    except (RuntimeError, PySnmpError) as err:
        print(err, "\n (can't access to devices?) Passing for now...")

def main():

    creds = get_snmp_v3_creds(SNMP_USR, SNMP_AUTH_PWD, SNMP_PRIV_PWD)

    prep_db_if_not_exist()

    while True:

        scrapped: List[Dict[str, str]] = get_all_nodes()
        devices: List[Tuple[str, str]] = []
        for device in scrapped:
            # This if has to be removed. It's just here since I added fake devices into db which are not scrappable 
            if 'iou' in device["device_name"]:
                devices.append((device["device_name"], None))

        if not devices:
            # Add an init node (should be an ENV var)
            devices.append(("sw1.iou", "192.168.77.1"))

        print(devices)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.wait(
                [
                    get_device_lldp_infos(hostname, NEEDED_MIBS.values(), creds, target_ip=ip) for hostname, ip in devices
                ]
            )
        )

        sleep(60)

if __name__ == "__main__":
    main()