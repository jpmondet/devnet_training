#! /usr/bin/env python3

from json import dumps
from requests import get, post, Response
from typing import Dict, List, Any, Tuple
from random import randint


PROJECT_NAME: str = "testapiproj"
GNS_SERVER: str = "http://192.168.56.1:3080/v2/"


def get_proj_id_or_create(name: str) -> str:

    data: Dict[str, str] = { "name": name }
    resp: Response = post(GNS_SERVER + "projects", data=dumps(data))
    if resp.status_code != 200:
        if resp.status_code == 409:
            #project exists
            resp = get(GNS_SERVER + "projects").json()
            for proj in resp:
                if proj["name"] == name:
                    return proj["project_id"]
        print(resp)
        print(resp.__dict__)
        return ""


    proj_id: str = resp.json()["project_id"]

    return proj_id

def get_template(name: str) -> Dict[str, Any]:
    resp: Response = get(GNS_SERVER + "templates")
    if resp.status_code != 200:
        print(resp)
        print(resp.__dict__)
        return ""

    for tplate in resp.json():
        if tplate["name"] == name:
            return tplate

    return ""

def create_node(project_id: str, name: str, template_name: str = "l2sw", node_type: str = "iou", compute_id: str = "local") -> str:

    tplate: Dict[str, Any] = get_template(template_name)

    data: Dict[str, Any] = { "name": name, "node_type": node_type, "compute_id": compute_id, "x": randint(-1000,500), "y": randint(-300, 500), "properties": { "path": tplate["path"] } }
    resp: Response = post(GNS_SERVER + f"projects/{project_id}/nodes", data=dumps(data))
    if resp.status_code != 201:
        print(resp)
        print(resp.__dict__)
        return ""

    node_id: str = resp.json()["node_id"]

    return node_id

def create_nodes(project_id: str, sw_or_rtr: str, nb_to_create:int) -> List[str]:

    nodes_ids: List[str] = []
    tplate_name = "l2sw"

    if sw_or_rtr not in ['sw', 'rtr']:
        return []
    elif sw_or_rtr == 'rtr':
        tplate_name = "l3rtr"

    for nb in range(nb_to_create):
        node_id = create_node(project_id, f"{sw_or_rtr}{nb + 1}", template_name=tplate_name)
        nodes_ids.append(node_id)

    return nodes_ids

def create_link(project_id: str, node1_id: str, node2_id: str, adapter_port_node1_tuple: Tuple[int,int], adapter_port_node2_tuple: Tuple[int,int]) -> str:

    data_to_send: Dict[str, List[Dict[str, Any]]] = { "nodes": [{"adapter_number": adapter_port_node1_tuple[0], "node_id": node1_id, "port_number": adapter_port_node1_tuple[1]},
        {"adapter_number": adapter_port_node2_tuple[0], "node_id": node2_id, "port_number": adapter_port_node2_tuple[1]}]}

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
        neigh_right = i+1
        if neigh_right == len(nodes_ids):
            # I think there is a rotating index in a python lib for that. Have to check...(Maybe in "collections" ?)
            neigh_right = 0
        create_link(project_id, nodes_ids[i], nodes_ids[neigh_right], (0,neigh_right), (0,i))

def create_star_topo(project_id: str, central_node_id: str, nodes_ids: List[str]) -> None:
    """ Create a star topology around the first node of the list """

    for i, node_id in enumerate(nodes_ids):
        create_link(project_id, central_node_id, node_id, (1,i), (0,0))

def start_nodes(project_id: str, nodes_ids: List[str]) -> None:

    data_to_send: Dict[None] = {}

    resp: Response = post(GNS_SERVER + f"projects/{project_id}/nodes/start", data=dumps(data_to_send))
    if resp.status_code != 204:
        print(resp)
        print(resp.__dict__)
        return ""

def main() -> None:

    proj_id: str = get_proj_id_or_create(PROJECT_NAME)

    if proj_id:
        print(proj_id)
        # Now that we have to project id, we can do pretty much everything
        switches_ids: List[str] = create_nodes(proj_id, 'sw', 4)
            
        create_loop_topo(proj_id, switches_ids)

        all_nodes_ids: List[str] = []
        for sw_id in switches_ids:
            rtr_ids: List[str] = create_nodes(proj_id, 'rtr', 2)
            all_nodes_ids.extend(rtr_ids)
            create_star_topo(proj_id, sw_id, rtr_ids)
        
        all_nodes_ids.extend(switches_ids)

        start_nodes(proj_id, all_nodes_ids)
        




if __name__ == "__main__":
    main()
