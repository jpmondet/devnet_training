""" Handles db access and abstracts functions
that can be (and should be) abstracted """

#! /usr/bin/env python3

from re import compile as rcompile, IGNORECASE as rIGNORECASE
from typing import List, Dict, Any
from os import access, R_OK
from time import sleep
from json import load as jload
from json.decoder import JSONDecodeError
#from bson.json_util import dumps as bdumps, loads as bloads

from pymongo import MongoClient, UpdateMany, ASCENDING as MDBASCENDING
from pymongo.errors import BulkWriteError, DuplicateKeyError as MDDPK
from requests import get as rget
import requests.exceptions

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

IFACES_STATS: str = "ifaces_stats.json"


def _safe_load_json_file(filename: str):
    if not access(filename, R_OK):
        return None

    datas: List[Dict[str, Any]] = None
    try:
        with open(filename, "r") as fp:
            datas = jload(fp)
    except JSONDecodeError:
        return None

    return datas


class NetworkError(RuntimeError):
    pass


def _retryer(max_retries=10, timeout=5):
    def wraps(func):
        request_exceptions = (
            requests.exceptions.Timeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError,
            requests.exceptions.SSLError,
        )

        def inner(*args, **kwargs):
            for i in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                except request_exceptions:
                    sleep(timeout * i)
                    continue
                else:
                    return result
            else:
                raise NetworkError

        return inner

    return wraps


def prep_db_if_not_exist():
    """If db is empty, with try to fill it with flat json files we may have from previous
    iterations."""

    if (
        get_entire_collection(STATS_COLLECTION)
        #and get_entire_collection(NODES_COLLECTION)
        and get_entire_collection(SCRAPPED_DEVICES_COLLECTION)
    ):
        # Looks like everything is already migrated and ready
        # Caching those answer and leaving :)
        return

    print("Preping db with flat files since at least one collection is empty")

    # We ensure that ids will be unique
    # (this is a mongodb feature)
    #STATS_COLLECTION.create_index({"device_id": 1, "iface_id": 1, "timestamp": 1}, unique=True)

    ifaces_stats = _safe_load_json_file(IFACES_STATS)
    if ifaces_stats:
        STATS_COLLECTION.insert_many(ifaces_stats)

    if not get_entire_collection(INDEX_SEQUENCE):
        INDEX_SEQUENCE.insert_one({"id": 0})

    # Leaderboards are lil' more specific since they were stored in customs
    # Thus we have to do more processing here to extract lboards
    if not get_entire_collection(NODES_COLLECTION) or not get_entire_collection(
        STATS_COLLECTION
    ):

        # We leverage this migration to use data from
        # Ragnasong website

        # First we get all the maps on the website
        rs_maps: List[Dict[str, Any]] = get_all_maps_from_api()
        # We add them to our db since this is the new source of truth
        try:
            STATS_COLLECTION.insert_many(rs_maps)
        except BulkWriteError as bwe:
            if "E11000 duplicate key error collection" in str(bwe):
                pass
            else:
                print(bwe)
                return

        csongs = _safe_load_json_file(IFACES_STATS)

        if csongs:
            # We try to get the old leaderboards to map them to the new source of truth is possible
            for cs in csongs:
                if cs["leaderboard"]:
                    rsmap: Dict[str, Any] = get_map_by_name(cs["name"], cs["band"])
                    if not rsmap:
                        print(cs)
                        continue

                    # Instead of storage a list, we use the power of mongodb and just store records
                    # Should help later to retrieve just what's needed and not the whole list
                    for score in cs["leaderboard"]:
                        lb_to_add = score.copy()
                        lb_to_add["map_uuid"] = rsmap["uuid"]
                        NODES_COLLECTION.insert_one(lb_to_add)

    if not get_entire_collection(LINKS_COLLECTION):
        acc = _safe_load_json_file("")
        players_details = _safe_load_json_file("")

        if acc and players_details:
            player_name_id = {}
            for pdetails in players_details:
                # We keep it temporary in player_name_id to migrate it to account just after
                pdetails["id"] = get_last_index_from_index_sequence()
                player_name_id[pdetails["name"]] = pdetails

            # Take the chance to update the dict to be mongodb-friendly
            # by adding an id instead of using a value as key
            acc_updated = []
            for discord_id, player_name in acc.items():
                pdetails = player_name_id[player_name]
                acc_updated.append(
                    {
                        "discord_id": discord_id,
                        "player_id": pdetails["id"],
                        "player_name": player_name,
                        "total_misses": 0,
                        "total_perfects_percent": 0.0,
                        "total_score": 0.0,
                        "total_triggers": 0,
                    }
                )
            LINKS_COLLECTION.insert_many(acc_updated)

    # Now that we have migrated all data, we suppress redondant datas that are still in leaderboards collection
    scores = get_entire_collection(NODES_COLLECTION)
    for score in scores:
        if not score.get("map_name"):
            continue
        score_updated = score.copy()
        account = get_account_by_discord_id(score["player_discord_id"])
        score_updated["player_id"] = account["player_id"]
        score_updated["difficulty_played"] = score["difficulty"]
        del score_updated["map_name"]
        del score_updated["band"]
        del score_updated["mapper"]
        del score_updated["player_name"]
        del score_updated["player_discord_id"]
        del score_updated["player_discord_name"]
        del score_updated["difficulty"]
        # NODES_COLLECTION.update_one(score, { '$set': score_updated })
        NODES_COLLECTION.find_one_and_replace(score, score_updated)
        # We also take this chance to update account stats:
        account["total_score"] = float(account["total_score"]) + float(score["score"])
        account["total_perfects_percent"] = float(account["total_perfects_percent"]) + float(
            score["perfects_percent"]
        )
        account["total_misses"] = int(account["total_misses"]) + int(score["misses"])
        account["total_triggers"] = int(account["total_triggers"]) + int(score["triggers"])
        del account["_id"]
        update_multiple_value_on_account_by_player_id(account["player_id"], account)


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
    #return IFACES_COLLECTION.find_one({ "device_name": device_name, "iface_name": iface_name })
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


def get_account_by_discord_id(discord_id: int) -> Dict[str, Any]:
    return LINKS_COLLECTION.find_one({"discord_id": str(discord_id)})


def get_account_by_player_id(player_id: int) -> Dict[str, Any]:
    return LINKS_COLLECTION.find_one({"player_id": player_id})


def get_accounts() -> List[Dict[str, Any]]:
    return get_entire_collection(LINKS_COLLECTION)


def get_pending_submissions() -> List[Dict[str, Any]]:
    return NODES_COLLECTION.find({})


def get_pending_submissions_by_player_id(player_id: int) -> List[Dict[str, Any]]:
    return NODES_COLLECTION.find({"player_id": player_id})


def get_map_by_name(title: str, artist: str) -> Dict[str, Any]:
    # This can be dangerous if there are multiple maps with the same name
    # It will be used only for migration purpose
    return STATS_COLLECTION.find_one({"title": title, "artist": artist})


def get_scores_by_player_id(player_id: int) -> List[Dict[str, Any]]:
    return NODES_COLLECTION.find({"player_id": player_id})


def get_score_by_map_uuid_and_diff(map_uuid: str, difficulty: str) -> List[Dict[str, Any]]:
    return NODES_COLLECTION.find({"map_uuid": map_uuid, "difficulty_played": difficulty})


def get_score_by_player_id_map_uuid_diff(
    player_id: int, map_uuid: str, difficulty: str
) -> Dict[str, Any]:
    return NODES_COLLECTION.find_one(
        {"player_id": player_id, "map_uuid": map_uuid, "difficulty_played": difficulty}
    )


def get_map_by_uuid(uuid: str) -> Dict[str, Any]:
    return STATS_COLLECTION.find_one({"uuid": uuid})


@_retryer()
def get_from_api(url: str) -> Dict[str, Any]:
    try:
        return rget(url).json()
    except JSONDecodeError:
        return {}


def get_all_maps_from_api() -> List[Dict[str, Any]]:
    try:
        start_count: int = 0
        resp: Dict[str, Any] = get_from_api(IFACES_STATS.format(start_count))
        nb_resp: int = len(resp["results"])
        rs_maps: List[Dict[str, Any]] = resp["results"]
        for start_count in range(nb_resp, resp["count"] + 1, nb_resp):
            resp = get_from_api(IFACES_STATS.format(start_count))
            rs_maps.extend(resp["results"])
        return rs_maps
    except NetworkError:
        return []


def get_new_maps_from_api() -> List[Dict[str, Any]]:
    current_maps = STATS_COLLECTION.find({})
    rs_maps = get_all_maps_from_api()

    current_maps_uuids = {dcm["uuid"]: dcm for dcm in current_maps}
    rs_maps_uuids = {dcm["uuid"]: dcm for dcm in rs_maps}

    uuids_to_add = set(rs_maps_uuids.keys()).difference(set(current_maps_uuids.keys()))
    print(uuids_to_add)

    maps_to_add = [rs_maps_uuids[uuid] for uuid in uuids_to_add]
    print(maps_to_add)

    return maps_to_add


def search_account_by_name(player_name: str):
    return LINKS_COLLECTION.find({"player_name": rcompile(player_name, rIGNORECASE)})


def search_map_by_title_artist_mapper(title: str, artist: str, mapper: str) -> List[Dict[str, Any]]:
    return STATS_COLLECTION.find(
        {
            "$and": [
                {"title": rcompile(title, rIGNORECASE)},
                {"artist": rcompile(artist, rIGNORECASE)},
                {"ownerUsername": rcompile(mapper, rIGNORECASE)},
            ]
        }
    )


def search_map_by_pattern(pattern: str):
    return STATS_COLLECTION.find(
        {
            "$or": [
                {"uuid": rcompile(pattern, rIGNORECASE)},
                {"title": rcompile(pattern, rIGNORECASE)},
                {"artist": rcompile(pattern, rIGNORECASE)},
                {"ownerUsername": rcompile(pattern, rIGNORECASE)},
                {"difficulty": rcompile(pattern, rIGNORECASE)},
                {"musicLink": rcompile(pattern, rIGNORECASE)},
            ]
        }
    )


def add_account(account: Dict[str, Any]) -> None:
    LINKS_COLLECTION.insert_one(account)

def add_iface_stats_at_time(device_name: str, iface_name: str, timestamp: int, stats: Dict[str, Any]) -> None:
    stats_line: Dict[str, Any] = {"device_name": device_name, "iface_name":iface_name}
    stats_line.update(stats)
    STATS_COLLECTION.insert_one(stats_line)

def add_iface_stats(stats: Dict[str, Any]) -> None:
    STATS_COLLECTION.insert_many(stats)


def add_pending_submission(submission: Dict[str, Any]) -> None:
    NODES_COLLECTION.insert_one(submission)


def add_score_to_cslboard(submission: Dict[str, Any]) -> None:
    NODES_COLLECTION.insert_one(submission)


def add_map_to_custom_songs(map_to_add: Dict[str, Any]) -> None:
    STATS_COLLECTION.insert_one(map_to_add)


def add_multiple_maps_to_custom_songs(maps_to_add: List[Dict[str, Any]]) -> None:
    STATS_COLLECTION.insert_many(maps_to_add)

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


def update_multiple_value_on_account_by_player_id(
    player_id: int, replace_query: Dict[str, Any]
) -> None:
    update_set_collection(LINKS_COLLECTION, {"player_id": player_id}, replace_query)


def update_account_by_player_id(player_id: int, attr_to_set: str, attr_value: Any) -> None:
    update_set_collection(LINKS_COLLECTION, {"player_id": player_id}, {attr_to_set: attr_value})


def update_map_by_uuid(uuid: str, attr_to_set: str, attr_value: Any) -> None:
    update_set_collection(STATS_COLLECTION, {"uuid": uuid}, {attr_to_set: attr_value})


def delete_account(player_id: int) -> None:
    LINKS_COLLECTION.delete_one({"player_id": player_id})


def delete_scores_on_lboard_by_player_id(player_id: int) -> None:
    NODES_COLLECTION.delete_many({"player_id": player_id})


def delete_pending_submission(submission: Dict[str, Any]) -> None:
    NODES_COLLECTION.delete_one(submission)
