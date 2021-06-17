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

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from time import strftime, localtime, time
from secrets import compare_digest

from fastapi import Depends, FastAPI, HTTPException, status, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger

from db_layer import (
    get_stats_devices,
    get_all_nodes,
    get_all_links,
    get_links_device,
    get_all_highest_utilizations,
    get_all_speeds
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

#API_USER: str = "user"
#API_PASS: str = "pass"

#security = HTTPBasic()  # TODO: Needs better security

CACHE: Dict[str, Any] = {}
CACHED_TIME: int = 300
TIME: int = int(time())
TIMEOUT: bool = True


#def check_credentials(credentials: HTTPBasicCredentials = Depends(security)):
#    correct_username = compare_digest(credentials.username, API_USER)
#    correct_password = compare_digest(credentials.password, API_PASS)
#    if not (correct_username and correct_password):
#        raise HTTPException(
#            status_code=status.HTTP_401_UNAUTHORIZED,
#            detail="Incorrect email or password",
#            headers={"WWW-Authenticate": "Basic"},
#        )
#    return credentials


def get_from_db_or_cache(element: str, func=None, query=None):
    global TIMEOUT, CACHE
    if not CACHE.get(element) or TIMEOUT:
        if not func:
            return None
        logger.error(f"Oops, {element} not in cache, calling db")
        if query:
            CACHE[element] = func(query)
        else:
            CACHE[element] = func()
        TIMEOUT = False

    return CACHE[element]


def background_time_update():
    global TIMEOUT, TIME
    now: int = int(time())
    logger.error(f'bgtimeupd: {now}, {TIME}, {TIMEOUT}')
    if now - TIME > CACHED_TIME:
        TIMEOUT = True
        TIME = now
    logger.error(f'bgtimeupdEnd: {now}, {TIME}, {TIMEOUT}')


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
                    "speed": "1",
                    "target": "deviceName-2",
                    "target_interfaces": [
                        "Ethernet0/0"
                    ],
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
    background_time_update()
    # logger.error(f"Caching timeout : {TIMEOUT}")

    nodes: List[Dict[str, Any]] = get_from_db_or_cache("nodes", get_all_nodes)

    for node in nodes:
        if not node.get("group") or not node.get("image"):
            # Test nodes
            if "sw" in node["device_name"]:
                node["group"] = 1
                node["image"] = "switch.png"
            else:
                node["group"] = 2
                node["image"] = "router.png"

        node["id"] = node["device_name"]

        try:
            del node["_id"]  # removing mongodb objectId
        except KeyError:
            pass

    formatted_links: Dict[str, Any] = get_from_db_or_cache("formatted_links")
    if not formatted_links:
        links: Dict[str, Any] = get_from_db_or_cache("links", get_all_links)
        sorted_links: List[Dict[str, Any]] = sorted(
            links, key=lambda d: (d["device_name"], d["neighbor_name"])
        )
        formatted_links = {}

        utilizations = get_from_db_or_cache("utilizations", get_all_highest_utilizations)
        speeds = get_from_db_or_cache("speeds", get_all_speeds)

        logger.error(utilizations)
        logger.error(speeds)

        # start_format_timer = time()

        logger.error(f'Nb links to format:{len(sorted_links)}')
        for link in sorted_links:
            device = link["device_name"]
            iface = link["iface_name"]
            neigh = link["neighbor_name"]
            neigh_iface = link["neighbor_iface"]

            id_link = device + neigh
            id_link_neigh = neigh + device

            if not formatted_links.get(id_link) and not formatted_links.get(id_link_neigh):


                speed = speeds[device + iface]
                speed = speed * 1000000  # Convert speed to bits

                highest_utilization = utilizations[device + iface]
                highest_utilization = highest_utilization * 8  # convert to bits
                percent_highest = highest_utilization / speed * 100
                logger.error(f'{device}, {iface}, {speed}, {highest_utilization}, {percent_highest}')

                f_link = {
                    "highest_utilization": percent_highest,
                    "source": device,
                    "source_interfaces": [iface],
                    "speed": speed,
                    "target": neigh,
                    "target_interfaces": [neigh_iface],
                }
                formatted_links[id_link] = f_link
            else:
                try:
                    if iface not in formatted_links[id_link]["source_interfaces"]:
                        formatted_links[id_link]["source_interfaces"].append(iface)
                    if neigh_iface not in formatted_links[id_link]["target_interfaces"]:
                        formatted_links[id_link]["target_interfaces"].append(neigh_iface)
                except KeyError:
                    if neigh_iface not in formatted_links[id_link_neigh]["source_interfaces"]:
                        formatted_links[id_link_neigh]["source_interfaces"].append(neigh_iface)
                    if iface not in formatted_links[id_link_neigh]["target_interfaces"]:
                        formatted_links[id_link_neigh]["target_interfaces"].append(iface)

        # logger.error(formatted_links)
        # logger.error(f'Format links End: {time() - start_format_timer}')

        global CACHE
        CACHE["formatted_links"] = formatted_links

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
    background_time_update()

    if isinstance(q, list):
        # Validate incoming query
        for device in q:
            if not isinstance(device, str):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            # if len(device) != 7 and len(device) != 8:
            #    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
            # if "iou" not in device:
            #    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        stats_by_device: Dict[str, Any] = get_from_db_or_cache(f"stats_by_device_{q}")

        if not stats_by_device:
            
            stats_by_device = {}

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
                    prev_timestamp: int = int(
                        datetime.strptime(prev_date, "%y-%m-%d %H:%M:%S").timestamp()
                    )
                    prev_inbits: int = stats_by_device[dname][ifname]["stats"][-1]["InSpeed"]
                    prev_outbits: int = stats_by_device[dname][ifname]["stats"][-1]["OutSpeed"]

                    interval = inttimestamp - prev_timestamp
                    if interval:
                        in_speed: int = inbits - prev_inbits
                        in_speed = in_speed if in_speed >= 0 else -in_speed
                        out_speed: int = outbits - prev_outbits
                        out_speed = out_speed if out_speed >= 0 else -out_speed
                        stat_formatted["InSpeed"] = int(in_speed / interval)
                        stat_formatted["OutSpeed"] = int(out_speed / interval)

                    stats_by_device[dname][ifname]["stats"].append(stat_formatted)

            global CACHE
            CACHE[f"stats_by_device_{q}"] = stats_by_device

        return stats_by_device

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/neighborships/")
# Leveraging query string validation built in FastApi to avoid having multiple IFs
def neighborships(
    q: str = Query(..., min_length=7, max_length=25)  # , regex="^[a-z]{2,3}[0-9]{1}.iou$")
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
    background_time_update()

    if not isinstance(q, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    neighs: List[Dict[str, str]] = get_from_db_or_cache(f"neighs_{q}")

    if not neighs:
        
        # We use a dict to prevent duplicates
        # The end goal is to return only its values, not keys
        neighs_dict: Dict[str, Dict[str, str]] = {}

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

            id_link = f'{device1}{device2}{iface1}{iface2}'
            if neighs_dict.get(id_link):
                continue

            neighs_dict[id_link] = {
                "local_intf": iface1,
                "neighbor": device2,
                "neighbor_intf": iface2,
            }
        
        neighs = list(neighs_dict.values())
        global CACHE
        CACHE[f"neighs_{q}"] = neighs

    return neighs


gunicorn_logger = logging.getLogger("gunicorn.info")
logger.handlers = gunicorn_logger.handlers
logger.setLevel(gunicorn_logger.level)