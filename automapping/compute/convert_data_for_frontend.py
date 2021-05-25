#!/usr/bin/python3
"""
    Inputs : 
        - graph_ct infos populated by lldp scrapping
        - interfaces infos populated by get_ifaces_stats that must be run regularly

    Expected output : 
        (see in respective GET methods : 
            graph,
            interfaces,
            neighborships
            no_neigh_ifaces,
            stats)
"""

from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Any, Optional
from ast import literal_eval
from time import strftime, localtime
from random import randint
from json import dump
from secrets import compare_digest

from fastapi import Depends, FastAPI, HTTPException, status, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from storage.db_layer import get_stats_devices, get_all_nodes, get_all_links, get_links_device, get_speed_iface, get_highest_utilization as db_highest_utilization

app = FastAPI()

origins = [
    "http://127.0.0.1",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

API_USER: str = "user"
API_PASS: str = "pass"

security = HTTPBasic() # TODO: Needs better security

LldpInfos = Dict[str, List[Dict[str, str]]]
IfacesStats = Dict[str, Dict[str, Dict[str, Dict[str, str]]]]
IfacesOutStruct = Dict[str, List[Dict[str, Any]]]
NeighsOutStruct = Dict[str, List[Dict[str, str]]]
GraphLinksStruct = List[Dict[str, Any]]

FRONTEND_DATA_DIR = "../frontend/public-html/data"

def check_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = compare_digest(credentials.username, API_USER)
    correct_password = compare_digest(credentials.password, API_PASS)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials

@app.get("/graph")
#def get_graph(credentials=Depends(check_credentials)):
def get_graph():
    """
                "links": [
                    {
                        "highest_utilization": 0,
                        "source": "deviceName",
                        "source_interfaces": [
                            "Ethernet0/0"
                        ],
                        //"source_interfaces_indes": [
                        //    1
                        //],
                        "speed": "1",
                        "target": "deviceName-2",
                        "target_interfaces": [
                            "Ethernet0/0"
                        ],
                        //"target_interfaces_indes": [
                        //    1
                        //]
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


        Graph shouldn't be updated very much
        However, "highest_utilization" must be updated each time the API is called
         with fresh "stats" values
    """

    nodes: List[Dict[str, Any]] = get_all_nodes()
    for node in nodes:
        node["group"] = 4 if 'sw' in node["device_name"] else 5
        node["id"] = node["device_name"]
        node["image"] = "default.png"
        del(node["_id"]) # removing mongodb objectId
    sorted_links: List[Dict[str, Any]] = sorted(get_all_links(), key=lambda d: (d['device_name'], d['neighbor_name']))
    formatted_links: Dict[str, Any] = {}
    for link in sorted_links:
        device = link["device_name"]
        iface = link["iface_name"]
        neigh = link["neighbor_name"]
        neigh_iface = link["neighbor_interface"]
        if not formatted_links.get(device+neigh) and not formatted_links.get(neigh+device):
            highest_utilization = db_highest_utilization(device, iface)
            speed = get_speed_iface(device, iface)
            percent_highest = int(int(highest_utilization) / int(speed))
            f_link = {
                "highest_utilization": percent_highest,
                "source": device,
                "source_interfaces": [iface],
                "speed": speed,
                "target": neigh,
                "target_interfaces": [neigh_iface],
            }
            formatted_links[device+neigh] = f_link
        else:
            try:
                if iface not in formatted_links[device+neigh]["source_interfaces"]:
                    formatted_links[device+neigh]["source_interfaces"].append(iface)
                if neigh_iface not in formatted_links[device+neigh]["target_interfaces"]:
                    formatted_links[device+neigh]["target_interfaces"].append(neigh_iface)
            except KeyError:
                if neigh_iface not in formatted_links[neigh+device]["source_interfaces"]:
                    formatted_links[neigh+device]["source_interfaces"].append(neigh_iface)
                if iface not in formatted_links[neigh+device]["target_interfaces"]:
                    formatted_links[neigh+device]["target_interfaces"].append(iface)

    return  { "nodes": nodes, "links": list(formatted_links.values()) }

#@app.get("/interfaces")
#def ifaces():
#    """
#    {
#       "deviceName": [
#           {
#               "ifDescr": "Ethernet0/0",
#               "ifSpeed": 10000,
#               "ifType": "ethernet",
#               "index": 1,
#           },
#           {},
#       ],
#       "deviceName2" : [],
#    } 
#    """
#    pass

#@app.get("/interfaces/{device_name}")
#def ifaces(device_name: str):
#    """
#    {
#       "deviceName": [
#           {
#               "ifDescr": "Ethernet0/0",
#               "ifSpeed": 10000,
#               "ifType": "ethernet",
#               "index": 1,
#           },
#           {},
#       ],
#       "deviceName2" : [],
#    } 
#    """
#    pass

@app.get("/stats/")
def stats(q: List[str] = Query(None)):
    """
                {
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
    # Interfaces names often have / in names...
    if isinstance(q, list):
        # Validate incoming query
        for device in q:
            if not isinstance(device, str):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            if len(device) != 7 and len(device) != 8:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            if 'iou' not in device:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        stats_by_device: Dict[str, Any] = {}
        sorted_stats = sorted(list(get_stats_devices(q)), key=lambda d: (d['device_name'], d['iface_name'], d['timestamp']))
        for stat in sorted_stats:
            dname = stat["device_name"]
            #ifname = stat["iface_name"].replace("Ethernet", "Et")
            ifname = stat["iface_name"]
            dbtime = stat["timestamp"]
            inttimestamp: int = int(dbtime)
            time = strftime("%y-%m-%d %H:%M:%S", localtime(inttimestamp))
            stat_formatted = { "InSpeed": 0, "OutSpeed": 0, "time": time}
            inbits: int = int(stat["in_bytes"]) * 8
            outbits: int = int(stat["out_bytes"]) * 8
            # This iface wasn't in the struct.
            # We add default infos (and speed to 0 since we don't know at how much speed it was before)
            if not stats_by_device.get(dname):
                stats_by_device[dname] = { ifname : { "ifDescr": ifname, "index": ifname, "stats": [stat_formatted]} }
            elif not stats_by_device[dname].get(ifname):
                stats_by_device[dname][ifname] = { "ifDescr": ifname, "index": ifname, "stats": [stat_formatted]}
            else:
                # Must calculate speed. Not just adding in_bytes or it will only increase.
                # Assuming it's ordered for now
                prev_date = stats_by_device[dname][ifname]["stats"][-1]["time"]
                prev_timestamp: int =  datetime.strptime(prev_date, "%y-%m-%d %H:%M:%S").timestamp()
                prev_inbits: int = stats_by_device[dname][ifname]["stats"][-1]["InSpeed"]
                prev_outbits: int = stats_by_device[dname][ifname]["stats"][-1]["OutSpeed"]

                interval = inttimestamp - prev_timestamp
                stat_formatted["InSpeed"] = int((inbits - prev_inbits) / interval)
                stat_formatted["OutSpeed"] = int((outbits - prev_outbits) / interval)

                stats_by_device[dname][ifname]["stats"].append(stat_formatted)
            
        return stats_by_device

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )

@app.get("/neighborships/")
# Leveraging query string validation built in FastApi to avoid having multiple IFs
def neighborships(q: str = Query(..., min_length=7, max_length=8, regex="^[a-z]{2,3}[0-9]{1}.iou$")):
    """
        {
                        "deviceName":[
                        "local_intf": "Ethernet0/0",
                        "neighbor": "deviceName2",
                        "neighbor_intf": "Ethernet0/0",
                    ],
                    "deviceName2" :[],
        }
    """
    neighs: List[Dict[str, str]] = []
    for link in get_links_device(q):
        device1: str = link["device_name"]
        device2: str = link["neighbor_name"]
        iface1: str = link["iface_name"]
        iface2: str = link["neighbor_interface"]
        # The device queried can be seen as "device_name" or as "neighbor_name" depending
        # on the point of view
        if q != link["device_name"]:
            device1, device2 = device2, device1
            iface1, iface2 = iface2, iface1

        neighs.append({ 
            "local_intf": iface1,
            "neighbor": device2,
            "neighbor_intf": iface2,
        })


    return neighs




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

            # Must calculate speed. Not just adding in_bytes or it will only increase.
            # Assuming it's ordered for now
            prev_timestamp: int = -1
            prev_inbits: int = -1
            prev_outbits: int = -1

            for timestamp, stats in iface_timed_infos.items():
                iface_det_stats: Dict[str, Any] = {}
                iface_details["ifSpeed"] = int(stats["bw"]) / 1000
                # Must calculate speed. Not just adding in_bytes or it will only increase.
                # Assuming it's ordered for now
                inttimestamp: int = int(timestamp)
                inbits: int = int(stats["in_bytes"]) * 8
                outbits: int = int(stats["out_bytes"]) * 8
                if prev_timestamp < 0:
                    inbits = 0
                    outbits = 0
                    iface_det_stats["InSpeed"] = inbits
                    iface_det_stats["OutSpeed"] = outbits
                else:
                    interval = int(timestamp) - prev_timestamp
                    iface_det_stats["InSpeed"] = int((inbits - prev_inbits) / interval)
                    iface_det_stats["OutSpeed"] = int((outbits - prev_outbits) / interval)
                iface_det_stats["time"] =  strftime("%Y-%m-%d %H:%M:%S", localtime(inttimestamp))
                iface_details["stats"].append(iface_det_stats)
                prev_timestamp = inttimestamp
                prev_inbits = inbits
                prev_outbits = outbits
            iface_index += 1
            ifaces_struct[device].append(iface_details)

    return ifaces_struct

def get_iface_infos(device_name: str, iface_name: str, ifaces_out_struct: IfacesOutStruct) -> Dict[str, Any]:
    for iface in ifaces_out_struct[device_name]:
        if iface["ifDescr"] == iface_name:
            return iface
    return {}

def get_highest_utilization(iface_left: Dict[str, Any], iface_right: Dict[str, Any]) -> int:
    """ Determine the highest utilization of a link depending on the interface stats 
    on both sides. The highest utilization is an integer representing a percentage """

    # Get highest speed iface
    highest_speed = iface_left["ifSpeed"] if iface_left["ifSpeed"] > iface_right["ifSpeed"] else iface_right["ifSpeed"]
    highest_speed = highest_speed * 1000000 # convert from Mbits to bits

    # Get highest last timestamp stats:
    iface_left_last = iface_left["stats"][-1]
    iface_left_highest = iface_left_last["InSpeed"]
    if iface_left_last["OutSpeed"] > iface_left_highest:
        iface_left_highest = iface_left_last["OutSpeed"]

    iface_right_last = iface_right["stats"][-1]
    iface_right_highest = iface_right_last["InSpeed"]
    if iface_right_last["OutSpeed"] > iface_right_highest:
        iface_right_highest = iface_right_last["OutSpeed"]

    highest_utilization = iface_left_highest if iface_left_highest > iface_right_highest else iface_right_highest 
    
    return int(highest_utilization / highest_speed * 100)

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
            link["highest_utilization"] = get_highest_utilization(iface_infos, iface_infos_nei)
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

def create_graph_struct(graph_links, ifaces_out_struct):
    graph_struct: Dict[str, List[Any]] = {}
    graph_struct["links"] = graph_links
    graph_struct["nodes"] = []
    # Will certainly put this into its own func to handle different images & stuff
    for device_name in ifaces_out_struct:
        graph_node = {}
        graph_node["group"] = 4 if "sw" in device_name else 5
        #graph_node["group"] = randint(1,6)
        graph_node["id"] = device_name
        graph_node["image"] = "default.png"
        graph_struct["nodes"].append(graph_node)
    
    return graph_struct


def write_into_appropriate_files(ifaces_out_struct: IfacesOutStruct, neigh_struct: NeighsOutStruct, graph_links: GraphLinksStruct) -> None:
    """ With all the datas formatted before, we write them for frontend requirements into : 
    graph.json, neighborships.json, no_neighbor_interfaces.json, interfaces.json, deviceName_ifaceIndex.json
    """

    # graph.json
    # Add 'nodes' to graph and write to file
    graph_struct: Dict[str, List[Any]] = {}
    graph_struct = create_graph_struct(graph_links, ifaces_out_struct)
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
