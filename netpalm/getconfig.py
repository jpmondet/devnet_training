#! /usr/bin/env python3

from os import getenv
from time import sleep
from json import dumps as jdumps
from concurrent.futures import ThreadPoolExecutor
import requests as req
from dotenv import load_dotenv

load_dotenv()
SRV = getenv("NETPALM_CTRL_URL")
API_KEY = getenv("NETPALM_API_KEY")
HEADERS = {
    "x-api-key": API_KEY,
    "accept": "application/json",
    "Content-Type": "application/json",
}

# For this example, only 1 switch is used..
SW_LOGIN = getenv("NETPALM_SW_LOGIN")
SW_PASS = getenv("NETPALM_SW_PASS")
SW_ADDR = getenv("NETPALM_SW_ADDR")
SW_PORT = getenv("NETPALM_SW_PORT")

# Connection Args are not THAT generic... (netmiko/napalm/etc. don't use same options keywords t_t)
GENERIC_BODY = {
    "library": "",
    "connection_args": {
        "device_type": "",
        "host": SW_ADDR,
        "username": SW_LOGIN,
        "password": SW_PASS,
        "optional_args": "",
    },
    "command": "",
    "args": {"use_textfsm": True},
    "queue_strategy": "pinned",
    "cache": {"enabled": True, "ttl": 300, "poison": False},
}


def launch_task(library, device_type, cmd):

    req_body = GENERIC_BODY.copy()
    req_body["library"] = library
    req_body["command"] = cmd
    req_body["connection_args"]["device_type"] = device_type

    # And here are the non-agnostic caveats again...
    if library == "netmiko":
        req_body["connection_args"]["port"] = SW_PORT
        del req_body["connection_args"]["optional_args"]
    elif library == "napalm":
        port = {"port": SW_PORT}
        req_body["connection_args"]["optional_args"] = port

    task = req.post(f"{SRV}/getconfig", headers=HEADERS, data=jdumps(req_body)).json()

    task_id = task["data"]["task_id"]

    print(f"Launched task for {cmd} with id: {task_id}")
    return task_id


def retrieve_result(task_id):

    status = "queued"
    while status != "finished":
        sleep(1)
        print(f"{task_id} still kicking...")
        task = req.get(f"{SRV}/task/{task_id}", headers=HEADERS).json()
        status = task["data"]["task_status"]

    if task["data"]["task_errors"]:
        print("oops")
        return "\n".join(task["data"]["task_errors"])

    return task["data"]["task_result"]


def main():

    task_ids = [
        launch_task("napalm", "cisco_nxos_ssh", "get_facts"),
        launch_task("netmiko", "cisco_nxos", "sh ip int b"),
    ]

    with ThreadPoolExecutor() as threxecutor:
        threads = [threxecutor.submit(retrieve_result, task_id) for task_id in task_ids]

    for thread in threads:
        print(jdumps(thread.result(), indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
