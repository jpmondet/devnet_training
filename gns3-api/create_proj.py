#! /usr/bin/env python3
""" Just playing with gns3 api for my own lab needs.
    This particular script:
        - creates a project (or use it if it already exists)
        - creates switches & routers
        - adds links between those nodes
        - starts the nodes
        - spawns consoles for all the nodes
        - inits all the nodes (mainly to bypass first config wizard)
        - brings up all interfaces
        - get cdp infos as a first check
"""

from json import dumps
from typing import Dict, List, Any, Tuple
from random import randint
from subprocess import call
from time import sleep

from requests import get, post, Response
from netmiko import ConnectHandler  # type: ignore
from netmiko.ssh_exception import NetmikoTimeoutException

# pylint: disable=missing-function-docstring

PROJECT_NAME: str = "testapiproj"
GNS_SERVER: str = "http://192.168.56.1:3080/v2/"


def get_proj_id_or_create(name: str) -> str:

    data: Dict[str, str] = {"name": name}
    resp: Response = post(GNS_SERVER + "projects", data=dumps(data))
    if resp.status_code != 200:
        if resp.status_code == 409:
            # project exists
            resp_json: List[Dict[str, Any]] = get(
                GNS_SERVER + "projects"
            ).json()
            for proj in resp_json:
                if proj["name"] == name:
                    proj_id: str = proj["project_id"]
                    return proj_id
        print(resp)
        print(resp.__dict__)
        return ""

    proj_id = resp.json()["project_id"]

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
    console_type: str = "telnet",
    custom_properties: Dict[str, Any] = {},
    ports: List[Dict[str, Any]] = None,
) -> str:

    tplate: Dict[str, Any] = get_template(template_name)
    if not custom_properties:
        if tplate.get("path"):
            custom_properties = {"path": tplate["path"]}

    data: Dict[str, Any] = {
        "name": name,
        "node_type": node_type,
        "compute_id": compute_id,
        "console_type": console_type,
        "x": randint(-1000, 500),
        "y": randint(-300, 500),
        "properties": custom_properties,
    }
    if ports:
        data["ports"] = ports

    resp: Response = post(
        GNS_SERVER + f"projects/{project_id}/nodes", data=dumps(data)
    )
    if resp.status_code != 201:
        print(resp)
        print(resp.__dict__)
        return ""

    node_id: str = resp.json()["node_id"]

    return node_id


def create_nodes(
    project_id: str, sw_or_rtr: str, nb_to_create: int
) -> List[str]:

    nodes_ids: List[str] = []
    tplate_name = "l2sw"

    if sw_or_rtr not in ["sw", "rtr"]:
        return []

    if sw_or_rtr == "rtr":
        tplate_name = "l3rtr"

    for num_node in range(nb_to_create):
        node_id = create_node(
            project_id, f"{sw_or_rtr}{num_node + 1}", template_name=tplate_name
        )
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

    resp: Response = post(
        GNS_SERVER + f"projects/{project_id}/links", data=dumps(data_to_send)
    )
    if resp.status_code != 201:
        print(resp)
        print(resp.__dict__)
        return ""

    link_id: str = resp.json()["link_id"]
    return link_id


def create_loop_topo(project_id: str, nodes_ids: List[str]) -> None:

    for i, _ in enumerate(nodes_ids):
        # Right & Left are based on clockwise rotation
        neigh_right = i + 1
        if neigh_right == len(nodes_ids):
            # I think there is a rotating index in a python lib for that.
            # Have to check...(Maybe in "collections" ?)
            neigh_right = 0
        create_link(
            project_id,
            nodes_ids[i],
            nodes_ids[neigh_right],
            (0, neigh_right),
            (0, i),
        )


def create_star_topo(
    project_id: str, central_node_id: str, nodes_ids: List[str]
) -> None:
    """ Create a star topology around the first node of the list """

    for i, node_id in enumerate(nodes_ids):
        create_link(project_id, central_node_id, node_id, (1, i), (0, 0))


def create_mgt_infra(project_id: str, nodes_ids: List[str]) -> None:
    """Create a 'cloud' device (which connect to the mgt station),
    and a simple switch to connect to all mgt interfaces
    and links everything"""

    # Create mgt nodes
    
    # cloud_gns3 is a custom template derived from the built-in
    # 'cloud' with only 1 'gns3' bridge iface
    port_map_struct : Dict[str, Any] = {
        "name": "gns3",   
        "special": True,
        "type": "ethernet"
    }
    ports_struct: Dict[str, Any] = {
        "adapter_number": 0,      
        "data_link_types": {      
          "Ethernet": "DLT_EN10MB"
        },                        
        "link_type": "ethernet",
        "name": "gns3",       
        "port_number": 0,         
        "short_name": "gns3"    
    }

    cloud_id: str = create_node(
        project_id, "cloud_gns3", template_name="cloud-gns3", node_type="cloud", console_type="none",
        custom_properties={"interfaces": [port_map_struct]} #, ports=[ports_struct]  <-- gns3 crash when adding this...
    )

    ports: List[Dict[str, Any]] = []
    for port in range(16):
        #port_struct = {                    
        #        "adapter_number": 0,    
        #        "data_link_types": {
        #            "Ethernet": "DLT_EN10MB"
        #            },
        #        "link_type": "ethernet",
        #        "name": f"Ethernet{port}",      
        #        "port_number": port,                    
        #        "short_name": f"e{port}"      
        #        }
        port_struct = {                     
              "name": f"Ethernet{port}",
              "port_number": port,   
              "type": "access",   
              "vlan": 1         
        }                  
        ports.append(port_struct)

    mgmt_sw_id: str = create_node(
        project_id,
        "mgmt_sw",
        template_name="ethswitch_gns3",
        node_type="ethernet_switch",
        console_type="none",
        #ports=ports
        custom_properties={ "ports_mapping": ports }
    )

    # Link both nodes
    create_link(project_id, cloud_id, mgmt_sw_id, (0, 0), (0, 0))
    for i, node_id in enumerate(nodes_ids):
        create_link(project_id, mgmt_sw_id, node_id, (0, i + 1), (1, 3))


def start_nodes(
    project_id: str, nodes_ids: List[str] = None  # type: ignore
) -> None:

    data_to_send: Dict[None, None] = {}

    if not nodes_ids:
        resp: Response = post(
            GNS_SERVER + f"projects/{project_id}/nodes/start",
            data=dumps(data_to_send),
        )
        if resp.status_code != 204:
            print(resp)
            print(resp.__dict__)
    else:
        # Start only the nodes specified
        pass


def console_to_nodes(
    project_id: str,
    nodes_ids: List[str] = None,  # type: ignore
    terminal_to_launch: str = "xfce4-terminal",
) -> None:
    # We assume to be on a linux machine.
    # Who would use something else anyways ? :troll:

    resp: Response = get(GNS_SERVER + f"projects/{project_id}/nodes")
    if resp.status_code != 200:
        print(resp)
        print(resp.__dict__)
        return

    for node in resp.json():
        if nodes_ids:
            if node["id"] not in nodes_ids:
                continue

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


def convert_nodes_list_to_inventory(
    nodes: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:

    inventory: List[Dict[str, Any]] = []

    for node in nodes:
        if node["node_type"] != "iou":
            continue
        node_data: Dict[str, Any] = {
            "device_type": "cisco_ios_telnet",
            "host": node["console_host"],
            "username": "",
            "password": "",
            "port": node["console"],
            "secret": "",
            "fast_cli": True,
        }
        inventory.append(node_data)

    return inventory


def connect_to_nodes(inventory: List[Dict[str, Any]]) -> List[ConnectHandler]:
    conns: List[ConnectHandler] = []

    for node in inventory:
        retries: int = 10
        con: ConnectHandler = None
        while not con:
            if retries == 0:
                print(f"Can't connect the node {node} :-/")
                # Will likely crash after that, but it's ok, it's just a lab
                break
            try:
                con = ConnectHandler(**node)
            except AttributeError:
                pass
            sleep(3)
            retries -= 1
        conns.append(con)

    return conns


def init_nodes(inventory: List[Dict[str, Any]]) -> None:

    conns: List[ConnectHandler] = connect_to_nodes(inventory)
    for con in conns:
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


def config_specific_node(con_to_node: ConnectHandler, cmds: List[str]) -> None:
    output: str = con_to_node.send_config_set(cmds)
    print(output)


def config_all_nodes(
    inventory: List[Dict[str, Any]], cmds: List[str]
) -> List[ConnectHandler]:
    conns: List[ConnectHandler] = connect_to_nodes(inventory)
    for con in conns:
        # for node in inventory:
        #    con: ConnectHandler = ConnectHandler(**node)
        #    con.enable()
        try:
            con.enable()
        except NetmikoTimeoutException:
            print("con already enabled")
        output: str = con.send_config_set(cmds)
        print(output)
    return conns


def get_from_all_nodes(
    inventory: List[Dict[str, Any]], cmds: List[str]
) -> None:
    conns: List[ConnectHandler] = connect_to_nodes(inventory)
    for con in conns:
        for cmd in cmds:
            output: str = con.send_command(cmd)
            print(output)
        con.disconnect()


def bring_up_ifaces(inventory: List[Dict[str, Any]]) -> None:
    configs: List[str] = ["lldp run", "int range e0/0-3,e1/0-3", "no shut"]
    config_all_nodes(inventory, configs)


def get_lldp_infos(inventory: List[Dict[str, Any]]) -> None:
    cmds: List[str] = ["sh lldp neigh"]
    get_from_all_nodes(inventory, cmds)


def prevent_console_timeouts(inventory: List[Dict[str, Any]]) -> None:
    configs: List[str] = [
        "line con 0",
        "exec-timeout 0",
        "session-timeout 0",
    ]
    config_all_nodes(inventory, configs)


def config_basics(
    inventory: List[Dict[str, Any]], nodes: List[Dict[str, Any]]
) -> None:
    configs: List[str] = [
        "line con 0",
        "exec-timeout 0",
        "session-timeout 0",
        "exit",
        "lldp run",
        "int range e0/0-3,e1/0-3",
        "no shut",
    ]
    conns = config_all_nodes(inventory, configs)

    iou_nodes = [node for node in nodes if node["node_type"] == "iou"]
    for index, node in enumerate(iou_nodes):
        configs = [
            f"hostname {node['name']}",
            "username iou privilege 15 secret iou",
            "ip domain name iou",
            "crypto key generate rsa modulus 1024 label iou",
            "ip ssh version 2",
            "int e1/3",
            "no switchport",
            f"ip addr 192.168.77.{ index + 1 } 255.255.255.0",
            "no lldp receive",
            "no lldp transmit",
            "exit",
            "line vty 0 4",
            "password iou",
            "privilege level 15",
            "transport input all",
        ]
        config_specific_node(conns[index], configs)


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

            create_mgt_infra(proj_id, all_nodes_ids)

        inventory: List[Dict[str, Any]] = convert_nodes_list_to_inventory(
            nodes
        )

        # Netmiko is a lil' slow, should use nornir instead
        # to do this in parallel
        if nodes[0]["status"] != "started":
            # Just for my tests:
            # I assume that if 1 node is started, all nodes are
            # (since I start them all together all the time for now):
            start_nodes(proj_id)
            sleep(5)
            console_to_nodes(proj_id)
            init_nodes(inventory)

            # bring_up_ifaces(inventory)
            # prevent_console_timeouts(inventory)  # Again, it's a lab ^^
            # config_hostname_and_mgt_ip(inventory)
            config_basics(inventory, nodes)

        get_lldp_infos(inventory)


if __name__ == "__main__":
    main()
