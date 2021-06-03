""" Handles db access and abstracts functions
that can be (and should be) abstracted """

#! /usr/bin/env python3

from re import compile as rcompile, IGNORECASE as rIGNORECASE
from typing import List, Dict, Any
#from bson.json_util import dumps as bdumps, loads as bloads

from pymongo import MongoClient, UpdateMany, ASCENDING as MDBASCENDING
from pymongo.errors import BulkWriteError, DuplicateKeyError as MDDPK

DB_STRING: str="mongodb://mongodb:27017/"
#DB_STRING: str="mongodb://127.0.0.1:27017/"

DB_CLIENT: MongoClient = MongoClient(DB_STRING)
DB = DB_CLIENT.automapping

# Collections used by discovery phase
# Devices retrieved by recursive lldp
SCRAPPED_DEVICES_COLLECTION = DB.scrappeddevices
# Devices that had an error while trying to connect
FAILED_DEVICES_COLLECTION = DB.faileddevices

# Collections that avoid data duplication (target)
# All nodes infos of the graph
NODES_COLLECTION = DB.nodes
# All ifaces Stats by devices
STATS_COLLECTION = DB.stats
# All ifaces current highest utilization (to colorize links accordingly)
UTILIZATION_COLLECTION = DB.utilization
# All links infos of the graph (neighborships)
LINKS_COLLECTION = DB.links

# Collection that only serves as an utility for other sequences
INDEX_SEQUENCE = DB.indexseq


def prep_db_if_not_exist():
    """If db is empty, we create db, collection & proper indexes."""

    if (
        get_entire_collection(NODES_COLLECTION)
        and get_entire_collection(LINKS_COLLECTION)
        and get_entire_collection(STATS_COLLECTION)
        and get_entire_collection(UTILIZATION_COLLECTION)
    ):
        # Looks like everything is ready
        # Caching frequent answers and leaving :)
        return

    print("Preping db since at least one collection is empty")

    # We ensure that ids will be unique
    # (this is a mongodb feature)
    NODES_COLLECTION.create_index({"device_name": 1}, unique=True)
    LINKS_COLLECTION.create_index({"device_name": 1, "iface_name": 1, "neighbor_name": 1, "neighbor_iface": 1}, unique=True)
    STATS_COLLECTION.create_index({"device_name": 1, "iface_name": 1, "timestamp": 1}, unique=True)
    UTILIZATION_COLLECTION.create_index({"device_name": 1, "iface_name": 1}, unique=True)

    if not get_entire_collection(INDEX_SEQUENCE):
        # Currently not in use but can be use to count indexes..
        INDEX_SEQUENCE.insert_one({"id": 0})


# In case we decide to use redis
#def set_in_cache(key, value):
#    CACHE_CLIENT.set(key, value)
#
#
#def get_from_cache(query):
#    entries = CACHE_CLIENT.get(query)
#    if entries:
#        print(f"Cache hit! ({query})")
#        entries = bloads(entries)
#    return entries


def get_entire_collection(mongodb_collection) -> List[Dict[str, Any]]:
    # entries: List[Dict, Any] = None
    # if mongodb_collection:
    #    entries = get_from_cache(mongodb_collection.name)
    # if not entries:
    #    entries =  list(mongodb_collection.find({}))
    #    if entries:
    #        print(f"Setting in cache ! ({mongodb_collection.name})")
    #        set_in_cache(mongodb_collection.name, bdumps(entries))
    return list(mongodb_collection.find({}))

def get_all_nodes() -> List[Dict[str, Any]]:
    return get_entire_collection(NODES_COLLECTION)

def get_all_links() -> List[Dict[str, Any]]:
    return get_entire_collection(LINKS_COLLECTION)

def get_links_device(device: str) -> List[Dict[str, Any]]:
    query: List[Dict[str, str]] = [{"device_name": device}, {"neighbor_name": device}]
    return LINKS_COLLECTION.find({"$or": query})

def get_nb_documents(mongodb_collection) -> int:
    return mongodb_collection.count_documents({})

def get_last_index_from_index_sequence() -> int:
    nb_doc = get_nb_documents(INDEX_SEQUENCE)
    INDEX_SEQUENCE.insert_one({"id": nb_doc})
    return nb_doc

def get_stats_devices(devices: List[str]):
    query: List[Dict[str, str]] = [{"device_name": device} for device in devices]
    return STATS_COLLECTION.find({"$or": query})

def get_speed_iface(device_name: str, iface_name: str):
    speed: int = 1
    try:
        speed = list(STATS_COLLECTION.find({ "device_name": device_name, "iface_name": iface_name }))[-1]["speed"]
    except KeyError:
        return 1
    return speed

def get_highest_utilization(device_name: str, iface_name: str):
    utilization_line = UTILIZATION_COLLECTION.find_one({ "device_name": device_name, "iface_name": iface_name })
    try:
        return utilization_line["last_utilization"]
    except (KeyError, TypeError):
        return 0
        
def search_device_by_name(device_name: str):
    return NODES_COLLECTION.find({"device_name": rcompile(device_name, rIGNORECASE)})

def search_device_by_name_and_ip(device_name: str, device_ip: str) -> List[Dict[str, Any]]:
    return NODES_COLLECTION.find(
        {
            "$and": [
                {"device_name": rcompile(device_name, rIGNORECASE)},
                {"device_ip": rcompile(device_ip, rIGNORECASE)},
            ]
        }
    )

def search_device_by_pattern(pattern: str):
    return NODES_COLLECTION.find(
        {
            "$or": [
                {"device_name": rcompile(pattern, rIGNORECASE)},
                {"device_ip": rcompile(pattern, rIGNORECASE)},
            ]
        }
    )

def add_iface_stats_at_time(device_name: str, iface_name: str, timestamp: int, stats: Dict[str, Any]) -> None:
    stats_line: Dict[str, Any] = {"device_name": device_name, "iface_name":iface_name}
    stats_line.update(stats)
    STATS_COLLECTION.insert_one(stats_line)

def add_iface_stats(stats: Dict[str, Any]) -> None:
    STATS_COLLECTION.insert_many(stats)

def bulk_update_collection(mongodb_collection, list_tuple_key_query) -> None:
    # Request is using UpdateMany (https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html?highlight=update#pymongo.collection.Collection.update_many)
    request: List[UpdateMany] = []
    for query, data in list_tuple_key_query:
        request.append(UpdateMany(query, { "$set": data }, True))

    mongodb_collection.bulk_write(request)

def update_collection(mongodb_collection, mongo_cmd, match_query, replace_query) -> None:
    mongodb_collection.update_many(match_query, {mongo_cmd: replace_query})


def update_set_collection(
    mongodb_collection, match_query: Dict[str, Any], replace_query: Dict[str, Any]
) -> None:
    update_collection(mongodb_collection, "$set", match_query, replace_query)


def delete_node(device_name: str) -> None:
    NODES_COLLECTION.delete_one({"device_name": device_name})

def delete_utilization_for_node_and_iface(device_name: str, iface_name: str) -> None:
    UTILIZATION_COLLECTION.delete_many({"device_name": device_name, "iface_name": iface_name})