""" Handles db access and abstracts functions
that can be (and should be) abstracted """

#! /usr/bin/env python3

from os import getenv
from re import compile as rcompile, IGNORECASE as rIGNORECASE
from typing import List, Dict, Any, Optional

from pymongo import MongoClient, UpdateMany, ASCENDING as MDBASCENDING # type: ignore
from pymongo.errors import BulkWriteError, DuplicateKeyError as MDDPK # type: ignore

DB_STRING: Optional[str] = getenv("DB_STRING")
if not DB_STRING:
    #DB_STRING = "mongodb://mongodb:27017/"
    DB_STRING = "mongodb://127.0.0.1:27017/"

DB_CLIENT: MongoClient = MongoClient(DB_STRING)
DB = DB_CLIENT.automapping

# Collections that avoid data duplication (target)
# All nodes infos of the graph
NODES_COLLECTION = DB.nodes
# All ifaces Stats by devices
STATS_COLLECTION = DB.stats
# All ifaces current highest utilization (to colorize links accordingly)
UTILIZATION_COLLECTION = DB.utilization
# All links infos of the graph (neighborships)
LINKS_COLLECTION = DB.links

def prep_db_if_not_exist():
    """If db is empty, we create proper indexes."""

    if (
        get_entire_collection(NODES_COLLECTION)
        and get_entire_collection(LINKS_COLLECTION)
        and get_entire_collection(STATS_COLLECTION)
        and get_entire_collection(UTILIZATION_COLLECTION)
    ):
        # Looks like everything is ready
        return

    print("Preping db since at least one collection is empty")

    # We ensure that entries will be unique
    # (this is a mongodb feature)
    NODES_COLLECTION.create_index({"device_name": 1}, unique=True)
    LINKS_COLLECTION.create_index({"device_name": 1, "iface_name": 1, "neighbor_name": 1, "neighbor_iface": 1}, unique=True)
    STATS_COLLECTION.create_index({"device_name": 1, "iface_name": 1, "timestamp": 1}, unique=True)
    UTILIZATION_COLLECTION.create_index({"device_name": 1, "iface_name": 1}, unique=True)

def get_entire_collection(mongodb_collection) -> List[Dict[str, Any]]:
    return list(mongodb_collection.find({}))

def get_all_nodes() -> List[Dict[str, Any]]:
    return get_entire_collection(NODES_COLLECTION)

def get_all_links() -> List[Dict[str, Any]]:
    return get_entire_collection(LINKS_COLLECTION)

def get_links_device(device: str) -> List[Dict[str, Any]]:
    query: List[Dict[str, str]] = [{"device_name": device}, {"neighbor_name": device}]
    return LINKS_COLLECTION.find({"$or": query})

def get_stats_devices(devices: List[str]):
    query: List[Dict[str, str]] = [{"device_name": device} for device in devices]
    return STATS_COLLECTION.find({"$or": query})

def get_speed_iface(device_name: str, iface_name: str):
    speed: int = 1
    try:
        speed = list(STATS_COLLECTION.find({ "device_name": device_name, "iface_name": iface_name }))[-1]["speed"]
    except (KeyError, IndexError) as err:
        print("oops? " + str(err))
        return 10
    return speed

def get_latest_utilization(device_name: str, iface_name: str):
    utilization_line = UTILIZATION_COLLECTION.find_one({ "device_name": device_name, "iface_name": iface_name })
    try:
        return utilization_line["last_utilization"]
    except (KeyError, TypeError):
        return 0

def get_highest_utilization(device_name: str, iface_name: str):
    utilization_line = UTILIZATION_COLLECTION.find_one({ "device_name": device_name, "iface_name": iface_name })
    try:
        utilization = utilization_line["last_utilization"] - utilization_line["prev_utilization"]
        return utilization
    except (KeyError, TypeError):
        return 0
        
def add_iface_stats(stats: List[Dict[str, Any]]) -> None:
    STATS_COLLECTION.insert_many(stats)

def bulk_update_collection(mongodb_collection, list_tuple_key_query) -> None:
    # Request is using UpdateMany (https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html?highlight=update#pymongo.collection.Collection.update_many)
    request: List[UpdateMany] = []
    for query, data in list_tuple_key_query:
        request.append(UpdateMany(query, { "$set": data }, True))

    mongodb_collection.bulk_write(request)