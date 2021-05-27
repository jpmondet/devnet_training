#! /usr/bin/env python3

from os import getenv
import asyncio
from itertools import groupby
from binascii import hexlify
from ast import literal_eval
from time import time, sleep
from typing import List, Dict, Any, Tuple
from pysnmp import hlapi
from pysnmp.entity.rfc3413.oneliner import cmdgen
#from dotenv import load_dotenv
from dpath.util import search
from storage.db_layer import (
    bulk_update_collection,
    add_iface_stats,
    STATS_COLLECTION,
    UTILIZATION_COLLECTION
)
#from utils.timing import timing

#load_dotenv(dotenv_path='../.env')

SNMP_USR = getenv("SNMP_USR")
SNMP_AUTH_PWD = getenv("SNMP_AUTH_PWD")
SNMP_PRIV_PWD = getenv("SNMP_PRIV_PWD")

CREDS = hlapi.UsmUserData(SNMP_USR, SNMP_AUTH_PWD, SNMP_PRIV_PWD,
        authProtocol=cmdgen.usmHMACSHAAuthProtocol,
        privProtocol=cmdgen.usmAesCfb128Protocol)
IFACES_TABLE_TO_COUNT = '1.3.6.1.2.1.2.1.0'
NEEDED_MIBS = { 
    'lldp': '1.0.8802.1.1.2.1.4.1', # LLDP neighs
    'iface_name': '1.3.6.1.2.1.2.2.1.2', # ifDescr
    'mtu': '1.3.6.1.2.1.2.2.1.4', # ifMtu
    'speed': '1.3.6.1.2.1.31.1.1.1.15', #ifHighSpeed
    'mac': '1.3.6.1.2.1.2.2.1.6', # ifPhysAddress
    'in_disc': '1.3.6.1.2.1.2.2.1.13', # ifInDiscards
    'in_err': '1.3.6.1.2.1.2.2.1.14', # ifInErrors
    'out_disc': '1.3.6.1.2.1.2.2.1.19', # ifOutDiscards
    'out_err': '1.3.6.1.2.1.2.2.1.20', # ifOutErrors
    'in_octets': '1.3.6.1.2.1.31.1.1.1.6', # ifHCInOctets
    'in_ucast_pkts': '1.3.6.1.2.1.31.1.1.1.7', # ifHCInUcastPkts
    'in_mcast_pkts': '1.3.6.1.2.1.31.1.1.1.8', # ifHCInMulticastPkts
    'in_bcast_pkts': '1.3.6.1.2.1.31.1.1.1.9', # ifHCInBroadcastPkts
    'out_octets': '1.3.6.1.2.1.31.1.1.1.10', # ifHCOutOctets
    'out_ucast_pkts': '1.3.6.1.2.1.31.1.1.1.11', # ifHCOutUcastPkts
    'out_mcast_pkts': '1.3.6.1.2.1.31.1.1.1.12', # ifHCOutMulticastPkts
    'out_bcast_pkts': '1.3.6.1.2.1.31.1.1.1.13', # ifHCOutBroadcastPkts
}

def construct_value_pairs(list_of_pairs):
    pairs = []
    for key, value in list_of_pairs.items():
        pairs.append(hlapi.ObjectType(hlapi.ObjectIdentity(key), value))
    return pairs

def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types

def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value

def fetch(handler, count):
    result = []
    for _ in range(count):
        try:
            error_indication, error_status, _, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result

def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]


def get_bulk(target, oids, credentials, count, start_from=0, port=161,
             engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.bulkCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        start_from, count,
        *construct_object_types(oids)
    )
    return fetch(handler, count)

#@timing
def dump_results_to_db(device_name, ifaces_infos) -> None:
    utilization_list: List[Tuple[Dict[str, str], Dict[str,str]]] = []
    stats_list: List[[Dict[str, str], Dict[str,str]]] = []
    for iface in ifaces_infos:
        _, ifname = next(search(iface, f"{NEEDED_MIBS['iface_name']}*", yielded=True))
        _, mtu = next(search(iface, f"{NEEDED_MIBS['mtu']}*", yielded=True))
        _, mac = next(search(iface, f"{NEEDED_MIBS['mac']}*", yielded=True))
        _, speed = next(search(iface, f"{NEEDED_MIBS['speed']}*", yielded=True))
        _, in_disc = next(search(iface, f"{NEEDED_MIBS['in_disc']}*", yielded=True))
        _, in_err = next(search(iface, f"{NEEDED_MIBS['in_err']}*", yielded=True))
        _, out_disc = next(search(iface, f"{NEEDED_MIBS['out_disc']}*", yielded=True))
        _, out_err = next(search(iface, f"{NEEDED_MIBS['out_err']}*", yielded=True))
        if ifname.startswith('Se') or ifname.startswith('Nu'):
            in_octets = 0
            in_ucast_pkts = 0
            speed = 10
        else: 
            _, in_octets = next(search(iface, f"{NEEDED_MIBS['in_octets']}*", yielded=True))
            _, in_ucast_pkts = next(search(iface, f"{NEEDED_MIBS['in_ucast_pkts']}*", yielded=True))
        _, in_mcast_pkts = next(search(iface, f"{NEEDED_MIBS['in_mcast_pkts']}*", yielded=True))
        _, in_bcast_pkts = next(search(iface, f"{NEEDED_MIBS['in_bcast_pkts']}*", yielded=True))
        _, out_octets = next(search(iface, f"{NEEDED_MIBS['out_octets']}*", yielded=True))
        _, out_ucast_pkts = next(search(iface, f"{NEEDED_MIBS['out_ucast_pkts']}*", yielded=True))
        _, out_mcast_pkts = next(search(iface, f"{NEEDED_MIBS['out_mcast_pkts']}*", yielded=True))
        _, out_bcast_pkts = next(search(iface, f"{NEEDED_MIBS['out_bcast_pkts']}*", yielded=True))

        iface_infos_dict = {
             'mtu': mtu,
             'mac': hexlify(mac.encode()).decode(),
             'speed': speed,
             'in_discards': in_disc,
             'in_errors': in_err,
             'out_discards': out_disc,
             'out_errors': out_err,
             'in_bytes': in_octets,
             'in_ucast_pkts': in_ucast_pkts,
             'in_mcast_pkts': in_mcast_pkts,
             'in_bcast_pkts': in_bcast_pkts,
             'out_bytes': out_octets,
             'out_ucast_pkts': out_ucast_pkts,
             'out_mcast_pkts': out_mcast_pkts,
             'out_bcast_pkts': out_bcast_pkts,
        }

        iface_name = "/".join("".join(x) for is_number, x in groupby(ifname, key=str.isdigit) if is_number is True)
        iface_stats_dict = {"device_name": device_name, "iface_name": iface_name, "timestamp": int(time())}
        iface_stats_dict.update(iface_infos_dict)
        stats_list.append(iface_stats_dict)
        # Each item of the lists are composed are the "query" (so the DB knows which entry to update
        # And the actual data
        query = {"device_name": device_name, "iface_name": iface_name}
        highest = int(iface_infos_dict["in_bytes"])
        lowest = int(iface_infos_dict["out_bytes"])
        if lowest > highest:
            highest = lowest
        utilization = {"device_name": device_name, "iface_name": iface_name, "last_utilization": highest}
        utilization_list.append((query, utilization))

    bulk_update_collection(UTILIZATION_COLLECTION, utilization_list)
    add_iface_stats(stats_list)

async def get_bulk_auto(target_name, oids, credentials, count_oid, start_from=0, port=161,
                  engine=hlapi.SnmpEngine(), context=hlapi.ContextData(), target_ip=None):
    
    target = target_ip if target_ip else target_name

    count = get(target, [count_oid], credentials, port, engine, context)[count_oid]
    res = get_bulk(target, oids, credentials, count, start_from, port, engine, context)

    dump_results_to_db(target_name, res)


def main():

    #test_devices = ['172.17.0.2', '172.17.0.2', '172.17.0.2']
    #test_devices = ['n9k.local.lab']
    #test_devices = ['192.168.77.1']

    scrapped: Dict[str, str] = {}
    with open("scrapped_devices") as sdf:
        scrapped = literal_eval(sdf.read())

    test_devices: List[Tuple[str, str]] = []
    for hostname, ip in scrapped.items():
        test_devices.append((hostname, ip))

    while True:

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.wait(
                [
                    #get_bulk_auto(device, NEEDED_MIBS.values(), CREDS, IFACES_TABLE_TO_COUNT) for device in test_devices
                    get_bulk_auto(hostname, NEEDED_MIBS.values(), CREDS, IFACES_TABLE_TO_COUNT, target_ip=ip) for hostname, ip in test_devices
                ]
            )
        )

        sleep(60)

if __name__ == "__main__":
    main()
