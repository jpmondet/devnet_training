#!/usr/bin/python3
"""
    Inputs : 
        - graph_ct infos populated by lldp scrapping
        - interfaces infos populated by get_ifaces_stats that must be run regularly

    Expected output : 
        - graph.json : {
                "links": [
                    {
                        "highest_utilization": 0,
                        "source": "deviceName",
                        "source_interfaces": [
                            "Ethernet0/0"
                        ],
                        "source_interfaces_indes": [
                            1
                        ],
                        "speed": "1",
                        "target": "deviceName-2",
                        "target_interfaces": [
                            "Ethernet0/0"
                        ],
                        "target_interfaces_indes": [
                            1
                        ]
                    },
                    {}],
                "nodes": [
                        {
                            group: 1,
                            id: "deviceName",
                            image: "default.png",
                        },
                        {}]
                }

        - neighborships.json: {
                    "deviceName":[
                        "local_intf": "Ethernet0/0",
                        "neighbor": "deviceName2",
                        "neighbor_intf": "Ethernet0/0",
                    ],
                    "deviceName2" :[],
                }
        - no_neighbor_interfaces.json: {
                    "deviceName": [
                        {
                            "ifDescr": "Ethernet0/0",
                            "ifSpeed": 10000,
                            "ifType": "ethernet",
                            "index": 1,
                        },
                        {},
                    ],
                    "deviceName2" : [],
                }
        - interfaces.json: {
                    "deviceName" : [
                        {
                            "ifDescr": "Ethernet0/0",
                            "ifSpeed": 10000,
                            "ifType": "ethernet",
                            "index": 1,
                        },
                        {},
                    ],
                    "deviceName2" : [],
                }
        - deviceName_ifaceIndex.json: {
                    "ifDescr": "Ethernet0/0",
                    "index": 1,
                    "stats": [
                        {
                            "InSpeed": 0,
                            "OutSpeed": 0,
                            "time": "2020-12-24 23:59:59"
                        },
                    ]
                }
"""

from typing import Dict, List, Any
from ast import literal_eval
from time import strftime, localtime
from random import randint
from json import dump

LldpInfos = Dict[str, List[Dict[str, str]]]
IfacesStats = Dict[str, Dict[str, Dict[str, Dict[str, str]]]]
IfacesOutStruct = Dict[str, List[Dict[str, Any]]]
NeighsOutStruct = Dict[str, List[Dict[str, str]]]
GraphLinksStruct = List[Dict[str, Any]]

FRONTEND_DATA_DIR = "./public-html/data"

def format_interfaces(ifaces_stats: IfacesStats) -> IfacesOutStruct:
    """ interfaces.json & deviceName_ifaceIndex.json being very similar, 
    we format interfaces for both of them """

    ifaces_struct: IfacesOutStruct = {}

    for device, iface_infos in ifaces_stats.items():
        ifaces_struct[device] = []
        iface_index: int = 0
        for iface_name, iface_timed_infos in iface_infos.items():
            iface_details: Dict[str, Any] = {}
            iface_details["ifDescr"] = iface_name
            iface_details["index"] = iface_index
            iface_details["stats"] = []
            for timestamp, stats in iface_timed_infos.items():
                iface_det_stats: Dict[str, Any] = {}
                iface_details["ifSpeed"] = int(stats["bw"]) / 1000
                iface_det_stats["InSpeed"] = int(stats["in_bytes"]) * 8
                iface_det_stats["OutSpeed"] = int(stats["out_bytes"]) * 8
                iface_det_stats["time"] =  strftime("%Y-%m-%d %H:%M:%S", localtime(int(timestamp)))
                iface_details["stats"].append(iface_det_stats)
            iface_index += 1
            ifaces_struct[device].append(iface_details)

    return ifaces_struct

def get_iface_infos(device_name: str, iface_name: str, ifaces_out_struct: IfacesOutStruct) -> Dict[str, Any]:
    for iface in ifaces_out_struct[device_name]:
        if iface["ifDescr"] == iface_name:
            return iface
    return {}

def format_neighborships(lldp_infos: LldpInfos, ifaces_out_struct: IfacesOutStruct) -> (NeighsOutStruct, GraphLinksStruct) :
    neighs: NeighsOutStruct = {}
    graph_links: GraphLinksStruct = []

    for device, neighs_device in lldp_infos.items():
        device_neighs: List[Dict[str, str]] = []
        for nei in neighs_device:
            # TODO: local_iface is called Etx/x in this lab case. Should find a cleaner way to sanitize this
            source_iface_name = f"Ethernet{nei['local_interface'][2:]}"
            iface_infos = get_iface_infos(device, source_iface_name, ifaces_out_struct)
            iface_infos_nei = get_iface_infos(nei["neighbor"], nei["port_descr"], ifaces_out_struct)

            link: Dict[str, Any] = {}
            link["highest_utilization"] = randint(1, 100) 
            link["source"] = device
            link["source_interfaces"] = [source_iface_name]
            link["source_interfaces_indes"] = [iface_infos["index"]]
            link["speed"] = iface_infos["ifSpeed"]
            link["target"] = nei["neighbor"]
            link["target_interfaces"] = [nei["port_descr"]]
            link["target_interfaces_indes"] = [iface_infos_nei["index"]]
            graph_links.append(link)

            device_nei: Dict[str, str] = {}
            device_nei["local_intf"] = source_iface_name
            device_nei["neighbor"] = nei["neighbor"]
            device_nei["neighbor_intf"] = nei["port_descr"]
            device_neighs.append(device_nei)
        neighs[device] = device_neighs

    return neighs, graph_links

def write_into_appropriate_files(ifaces_out_struct: IfacesOutStruct, neigh_struct: NeighsOutStruct, graph_links: GraphLinksStruct) -> None:
    """ With all the datas formatted before, we write them for frontend requirements into : 
    graph.json, neighborships.json, no_neighbor_interfaces.json, interfaces.json, deviceName_ifaceIndex.json
    """

    # graph.json
    # Add 'nodes' to graph and write to file
    graph_struct: Dict[str, List[Any]] = {}
    graph_struct["links"] = graph_links
    graph_struct["nodes"] = []
    # Will certainly put this into its own func to handle different images & stuff
    for device_name in ifaces_out_struct:
        graph_node = {}
        graph_node["group"] = randint(1,6)
        graph_node["id"] = device_name
        graph_node["image"] = "default.png"
        graph_struct["nodes"].append(graph_node)
    with open(f"{FRONTEND_DATA_DIR}/graph.json", "w") as gfile:
        dump(graph_struct, gfile)


    # neighborships.json & no_neighbor_interfaces.json
    with open(f"{FRONTEND_DATA_DIR}/neighborships.json", "w") as neifile:
        dump(neigh_struct, neifile)
    # I've no use for it for now so it'll be empty
    with open(f"{FRONTEND_DATA_DIR}/no_neighbor_interfaces.json", "w") as neifile:
        dump({}, neifile)


    # interfaces.json & deviceName_ifaceIndex.json
    for device_name, device_ifaces in ifaces_out_struct.items():
        for iface in device_ifaces:
            with open(f"{FRONTEND_DATA_DIR}/stats/{device_name}_{iface['index']}.json", "w") as device_file:
                dump(iface, device_file)
            del(iface["stats"])

    with open(f"{FRONTEND_DATA_DIR}/interfaces.json", "w") as int_file:
        dump(ifaces_out_struct, int_file)

    return None


def main() -> None:

    # {'sw1.iou': [{'mgmt_address': '192.168.77.4', 'neighbor': 'sw4.iou', 'port_descr': 'Ethernet0/0', 'neighbor_interface': 'Et0/0', 'mac': 'aabb.cc00.0400', 'local_interface': 'Et0/3'},
    lldp_infos: LldpInfos = {}
    with open("graph_ct", "r") as res:
        lldp_infos = literal_eval(res.read())

    # {"sw1.iou": {"Ethernet0/0": {"1607408237": {"out_packets": "2365", "out_bytes": "212667", "out_underruns": "0", "in_errors": "0", "in_crc": "0", "in_frame": "0", "in_overrun": "0", "in_ignored": "0", "in_packets": "0", "in_bytes": "0", "in_no_buffer": "0", "mtu": "1500", "bw": "10000", "delay": "1000", "mac": "aabb.cc00.0100", "bia_mac": "aabb.cc00.0100", "iface": "Ethernet0/0"},
    ifaces_stats: IfacesStats = {}
    with open("ifaces_stats.json", "r") as res:
        ifaces_stats = literal_eval(res.read())

    ifaces_out_struct = format_interfaces(ifaces_stats)

    neigh_struct, graph_links = format_neighborships(lldp_infos, ifaces_out_struct)

    write_into_appropriate_files(ifaces_out_struct, neigh_struct, graph_links)

if __name__ == "__main__":
    main()
