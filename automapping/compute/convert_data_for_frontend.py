#!/usr/bin/python3
"""
    Inputs : 
        - graph_ct infos populated by lldp scrapping
        - interfaces infos populated by get_ifaces_stats that must be run regularly

    Expected output : 
        (see in respective GET methods : 
            graph,
            stats,
            neighborships
        )
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from time import strftime, localtime
from secrets import compare_digest

from fastapi import Depends, FastAPI, HTTPException, status, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware

from storage.db_layer import (
    get_stats_devices,
    get_all_nodes,
    get_all_links,
    get_links_device,
    get_speed_iface,
    get_highest_utilization,
)

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
    allow_methods=["*"],
    allow_headers=["*"],
)

API_USER: str = "user"
API_PASS: str = "pass"

security = HTTPBasic()  # TODO: Needs better security

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
# def get_graph(credentials=Depends(check_credentials)):
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
        node["group"] = 1 if "sw" in node["device_name"] else 2 
        if node["device_name"].startswith('fake'):
            node['group'] = 3
        elif node["device_name"].startswith('down_fake'):
            node['group'] = 5

        node["id"] = node["device_name"]
        node["image"] = "default.png"
        del node["_id"]  # removing mongodb objectId
    sorted_links: List[Dict[str, Any]] = sorted(
        get_all_links(), key=lambda d: (d["device_name"], d["neighbor_name"])
    )
    formatted_links: Dict[str, Any] = {}
    for link in sorted_links:
        device = link["device_name"]
        iface = link["iface_name"]
        neigh = link["neighbor_name"]
        neigh_iface = link["neighbor_iface"]
        if not formatted_links.get(device + neigh) and not formatted_links.get(neigh + device):
            highest_utilization = get_highest_utilization(device, iface)
            speed = get_speed_iface(device, iface)
            speed = speed * 1000000 #Convert speed to bits
            highest_utilization = highest_utilization * 8 #convert to bits
            percent_highest = highest_utilization / speed * 100
            f_link = {
                "highest_utilization": percent_highest,
                "source": device,
                "source_interfaces": [iface],
                "speed": speed,
                "target": neigh,
                "target_interfaces": [neigh_iface],
            }
            formatted_links[device + neigh] = f_link
        else:
            try:
                if iface not in formatted_links[device + neigh]["source_interfaces"]:
                    formatted_links[device + neigh]["source_interfaces"].append(iface)
                if neigh_iface not in formatted_links[device + neigh]["target_interfaces"]:
                    formatted_links[device + neigh]["target_interfaces"].append(neigh_iface)
            except KeyError:
                if neigh_iface not in formatted_links[neigh + device]["source_interfaces"]:
                    formatted_links[neigh + device]["source_interfaces"].append(neigh_iface)
                if iface not in formatted_links[neigh + device]["target_interfaces"]:
                    formatted_links[neigh + device]["target_interfaces"].append(iface)

    return {"nodes": nodes, "links": list(formatted_links.values())}

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
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            if len(device) != 7 and len(device) != 8:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            if "iou" not in device:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        stats_by_device: Dict[str, Any] = {}
        sorted_stats = sorted(
            list(get_stats_devices(q)),
            key=lambda d: (d["device_name"], d["iface_name"], d["timestamp"]),
        )
        for stat in sorted_stats:
            dname = stat["device_name"]
            # ifname = stat["iface_name"].replace("Ethernet", "Et")
            ifname = stat["iface_name"]
            dbtime = stat["timestamp"]
            inttimestamp: int = int(dbtime)
            time = strftime("%y-%m-%d %H:%M:%S", localtime(inttimestamp))
            stat_formatted = {"InSpeed": 0, "OutSpeed": 0, "time": time}
            inbits: int = int(stat["in_bytes"]) * 8
            outbits: int = int(stat["out_bytes"]) * 8
            # This iface wasn't in the struct.
            # We add default infos (and speed to 0 since we don't know at how much speed it was before)
            if not stats_by_device.get(dname):
                stats_by_device[dname] = {
                    ifname: {"ifDescr": ifname, "index": ifname, "stats": [stat_formatted]}
                }
            elif not stats_by_device[dname].get(ifname):
                stats_by_device[dname][ifname] = {
                    "ifDescr": ifname,
                    "index": ifname,
                    "stats": [stat_formatted],
                }
            else:
                # Must calculate speed. Not just adding in_bytes or it will only increase.
                # Assuming it's ordered for now
                prev_date = stats_by_device[dname][ifname]["stats"][-1]["time"]
                prev_timestamp: int = datetime.strptime(prev_date, "%y-%m-%d %H:%M:%S").timestamp()
                prev_inbits: int = stats_by_device[dname][ifname]["stats"][-1]["InSpeed"]
                prev_outbits: int = stats_by_device[dname][ifname]["stats"][-1]["OutSpeed"]

                interval = inttimestamp - prev_timestamp
                if interval:
                    stat_formatted["InSpeed"] = int((inbits - prev_inbits) / interval)
                    stat_formatted["OutSpeed"] = int((outbits - prev_outbits) / interval)

                stats_by_device[dname][ifname]["stats"].append(stat_formatted)

        return stats_by_device

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/neighborships/")
# Leveraging query string validation built in FastApi to avoid having multiple IFs
def neighborships(
    q: str = Query(..., min_length=7, max_length=8)#, regex="^[a-z]{2,3}[0-9]{1}.iou$")
):
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
        iface2: str = link["neighbor_iface"]
        # The device queried can be seen as "device_name" or as "neighbor_name" depending
        # on the point of view
        if q != link["device_name"]:
            device1, device2 = device2, device1
            iface1, iface2 = iface2, iface1

        neighs.append(
            {"local_intf": iface1, "neighbor": device2, "neighbor_intf": iface2,}
        )

    return neighs

def main() -> None:
    # Used only for quick tests
    get_graph()


if __name__ == "__main__":
    main()
