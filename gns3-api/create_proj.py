#! /usr/bin/env python3

from json import dumps
from typing import Dict, List, Any, Tuple
from random import randint
from subprocess import call
from time import sleep

from requests import get, post, Response
from netmiko import ConnectHandler


PROJECT_NAME: str = "testapiproj"
GNS_SERVER: str = "http://192.168.56.1:3080/v2/"


def get_proj_id_or_create(name: str) -> str:

    data: Dict[str, str] = {"name": name}
    resp: Response = post(GNS_SERVER + "projects", data=dumps(data))
    if resp.status_code != 200:
        if resp.status_code == 409:
            # project exists
            resp = get(GNS_SERVER + "projects").json()
            for proj in resp:
                if proj["name"] == name:
                    return proj["project_id"]
        print(resp)
        print(resp.__dict__)
        return ""

    proj_id: str = resp.json()["project_id"]

    return proj_id


def get_template(name: str) -> Any:
    resp: Response = get(GNS_SERVER + "templates")
    if resp.status_code != 200:
        print(resp)
        print(resp.__dict__)
        return {}

    for tplate in resp.json():
        if tplate["name"] == name:
            return tplate

    return {}


def list_nodes(project_id: str) -> Any:

    resp: Response = get(GNS_SERVER + f"projects/{project_id}/nodes")

    if resp.status_code != 200:
        print(resp)
        print(resp.__dict__)
        return []

    return resp.json()


def create_node(
    project_id: str,
    name: str,
    template_name: str = "l2sw",
    node_type: str = "iou",
    compute_id: str = "local",
) -> str:

    tplate: Dict[str, Any] = get_template(template_name)

    data: Dict[str, Any] = {
        "name": name,
        "node_type": node_type,
        "compute_id": compute_id,
        "x": randint(-1000, 500),
        "y": randint(-300, 500),
        "properties": {"path": tplate["path"]},
    }
    resp: Response = post(GNS_SERVER + f"projects/{project_id}/nodes", data=dumps(data))
    if resp.status_code != 201:
        print(resp)
        print(resp.__dict__)
        return ""

    node_id: str = resp.json()["node_id"]

    return node_id


def create_nodes(project_id: str, sw_or_rtr: str, nb_to_create: int) -> List[str]:

    nodes_ids: List[str] = []
    tplate_name = "l2sw"

    if sw_or_rtr not in ["sw", "rtr"]:
        return []
    elif sw_or_rtr == "rtr":
        tplate_name = "l3rtr"

    for nb in range(nb_to_create):
        node_id = create_node(project_id, f"{sw_or_rtr}{nb + 1}", template_name=tplate_name)
        nodes_ids.append(node_id)

    return nodes_ids


def create_link(
    project_id: str,
    node1_id: str,
    node2_id: str,
    adapter_port_node1_tuple: Tuple[int, int],
    adapter_port_node2_tuple: Tuple[int, int],
) -> str:

    data_to_send: Dict[str, List[Dict[str, Any]]] = {
        "nodes": [
            {
                "adapter_number": adapter_port_node1_tuple[0],
                "node_id": node1_id,
                "port_number": adapter_port_node1_tuple[1],
            },
            {
                "adapter_number": adapter_port_node2_tuple[0],
                "node_id": node2_id,
                "port_number": adapter_port_node2_tuple[1],
            },
        ]
    }

    resp: Response = post(GNS_SERVER + f"projects/{project_id}/links", data=dumps(data_to_send))
    if resp.status_code != 201:
        print(resp)
        print(resp.__dict__)
        return ""

    link_id: str = resp.json()["link_id"]
    return link_id


def create_loop_topo(project_id: str, nodes_ids: List[str]) -> None:

    for i, node_id in enumerate(nodes_ids):
        # Right & Left are based on clockwise rotation
        neigh_right = i + 1
        if neigh_right == len(nodes_ids):
            # I think there is a rotating index in a python lib for that. Have to check...(Maybe in "collections" ?)
            neigh_right = 0
        create_link(project_id, nodes_ids[i], nodes_ids[neigh_right], (0, neigh_right), (0, i))


def create_star_topo(project_id: str, central_node_id: str, nodes_ids: List[str]) -> None:
    """ Create a star topology around the first node of the list """

    for i, node_id in enumerate(nodes_ids):
        create_link(project_id, central_node_id, node_id, (1, i), (0, 0))


def start_nodes(project_id: str, nodes_ids: List[str]) -> None:

    data_to_send: Dict[None, None] = {}

    resp: Response = post(
        GNS_SERVER + f"projects/{project_id}/nodes/start", data=dumps(data_to_send)
    )
    if resp.status_code != 204:
        print(resp)
        print(resp.__dict__)


def console_to_nodes(
    project_id: str, nodes_ids: List[str], terminal_to_launch: str = "xfce4-terminal"
) -> None:
    # We assume to be on a linux machine. Who would use something else anyways ? :troll:

    resp: Response = get(GNS_SERVER + f"projects/{project_id}/nodes")
    if resp.status_code != 200:
        print(resp)
        print(resp.__dict__)
        return None

    for node in resp.json():
        console_port: int = node["console"]
        console_ip: str = node["console_host"]
        console_type: str = node["console_type"]
        node_name: str = node["name"]
        call(
            [
                terminal_to_launch,
                "-T",
                f"{node_name}",
                "-x",
                f"{console_type}",
                f"{console_ip}",
                f"{str(console_port)}",
            ]
        )


def convert_nodes_list_to_inventory(nodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:

    inventory: List[Dict[str, Any]] = []

    for node in nodes:
        node_data: Dict[str, Any] = {
            "device_type": "cisco_ios_telnet",
            "host": node["console_host"],
            "username": "",
            "password": "",
            "port": node["console"],
            "secret": "",
        }
        inventory.append(node_data)

    return inventory


def init_nodes(inventory: List[Dict[str, Any]]) -> None:

    for node in inventory:
        retries: int = 10
        con: ConnectHandler = None
        while not con:
            if retries == 0:
                print("Hmm, something's not right...Can't init the nodes")
                return
            try:
                con = ConnectHandler(**node)
            except AttributeError:
                sleep(1)
            retries -= 1

        # Had to patch netmiko locally since it doesn't like telnet
        # without login & pass
        output: str = con.send_command_timing(
            command_string="\n", strip_prompt=False, strip_command=False
        )
        if "initial configuration" in output:
            output += con.send_command_timing(
                command_string="no \n", strip_prompt=False, strip_command=False
            )
        if "Would you like to terminate autoinstall" in output:
            output += con.send_command_timing(
                command_string="\n", strip_prompt=False, strip_command=False
            )
        print(output)


def config_all_nodes(inventory: List[Dict[str, Any]], cmds: List[str]) -> None:
    for node in inventory:
        con: ConnectHandler = ConnectHandler(**node)
        con.enable()
        output: str = con.send_config_set(cmds)
        print(output)


def get_from_all_nodes(inventory: List[Dict[str, Any]], cmds: List[str]) -> None:
    for node in inventory:
        con: ConnectHandler = ConnectHandler(**node)
        con.enable()
        for cmd in cmds:
            output: str = con.send_command(cmd)
            print(output)


def bring_up_ifaces(inventory: List[Dict[str, Any]]) -> None:
    configs: List[str] = ["int range e0/0-3,e1/0-3", "no shut"]
    config_all_nodes(inventory, configs)


def get_cdp_infos(inventory: List[Dict[str, Any]]) -> None:
    cmds: List[str] = ["sh cdp neigh"]
    get_from_all_nodes(inventory, cmds)


def main() -> None:

    proj_id: str = get_proj_id_or_create(PROJECT_NAME)

    if proj_id:
        print(proj_id)
        # Now that we have to project id, we can do pretty much everything

        all_nodes_ids: List[str] = []
        nodes: List[Dict[str, Any]] = list_nodes(proj_id)

        if nodes:
            # For my tests, I dun need to recreate all nodes all the time:
            for node in nodes:
                all_nodes_ids.append(node["node_id"])
        else:
            switches_ids: List[str] = create_nodes(proj_id, "sw", 4)

            create_loop_topo(proj_id, switches_ids)

            for sw_id in switches_ids:
                rtr_ids: List[str] = create_nodes(proj_id, "rtr", 2)
                all_nodes_ids.extend(rtr_ids)
                create_star_topo(proj_id, sw_id, rtr_ids)

            all_nodes_ids.extend(switches_ids)
            nodes = list_nodes(proj_id)

        inventory: List[Dict[str, Any]] = convert_nodes_list_to_inventory(nodes)

        if nodes[0]["status"] != "started":
            # Just for my tests, I assume that if 1 node is started, all nodes are (since I start them all together all the time for now):
            start_nodes(proj_id, all_nodes_ids)
            sleep(5)
            console_to_nodes(proj_id, all_nodes_ids)
            init_nodes(inventory)
            bring_up_ifaces(inventory)

        get_cdp_infos(inventory)


if __name__ == "__main__":
    main()
