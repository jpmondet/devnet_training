#!/usr/bin/python3
""" Drawing topology from datas retrieved 
    from recursive LLDP scrapping runs
"""
from ast import literal_eval

from networkx import Graph, drawing, set_node_attributes, compose_all
from plotly import graph_objs
from plotly.offline import plot
from chart_studio import plotly

def add_node_to_graph(graph, device, nei_infos):
    graph.add_node(device)
    for nei in nei_infos:
        nei_name = nei["neighbor"].lower()
        # Placeholder if we want to discard some specific devices from the drawings
        to_discard = ["names-that-we-want-to-discard"]

        if any(sub_name in nei_name for sub_name in to_discard):
            print("Discarding {} to have a cleaner graph. Remove it from the 'discard' list if you still want this device.".format(nei_name))
            with open("discarded_devices", "a") as fdiscard:
                fdiscard.write(nei_name)
            continue

        try:
            graph.add_node(
                nei["neighbor"].lower(),
                #system=nei["system_description"],  # , ip=nei["mgmt_address"]
                ip=nei["mgmt_address"]
            )
            graph.add_edge(
                device,
                nei["neighbor"].lower(),
                iface=nei["local_interface"],
                remote_iface=nei["neighbor_interface"],
            )
        except TypeError:
            print("Skipping the badly formated NEIGHBOR of the device : {}".format(device))
            print("Bad formatted nei : " + str(nei))
        except KeyError:
            print("Skipping the badly formated NEIGHBOR of the device : {}".format(device))
            print("Bad formatted nei : " + str(nei))
    return graph


def add_to_proper_graph(device, nei, *graphs):
    """ When using the 'multigraphs' feature, we must determine
    which node goes where.
    This is something that you should adjust to your own topology since
    we all have different needs """

    graphs = graphs[0]
    graph1 = graphs[0]
    graph2 = graphs[1]
    graph3 = graphs[2]
    graph4 = graphs[3]
    graph5 = graphs[4]
    if "sw" in device:
        graph1.add_node(device)
    elif "rtr" in device:
        graph2.add_node(device)
    else:
        print("Ignoring {}".format(device))

    return graph1, graph2, graph3, graph4, graph5

def create_frontend_graph(formatted_results, multigraphs):

    tmp_graph = Graph()

    for device, nei_infos in formatted_results.items():
        tmp_graph = add_node_to_graph(tmp_graph, device, nei_infos)

    # Separate nodes in multiple graphs to have cleaner drawings
    # Those graphs will then be re-merged
    # This step can be bypassed if not needed by passing
    # False to "multigraphs"
    if multigraphs:
        graph1 = Graph()
        graph2 = Graph()
        graph3 = Graph()
        graph4 = Graph()
        graph5 = Graph()
        graphs = [graph1, graph2, graph3, graph4, graph5]  
        for device, nei in list(tmp_graph.edges):
            graphs = add_to_proper_graph(device, nei, graphs)
            graphs = add_to_proper_graph(nei, device, graphs)

        # Trying to avoid overlapping of different zones
        # Yeah, this is ugly, but algorithms that generate graphs do some...
        # Unexpected things :-\ 
        positions1 = drawing.layout.fruchterman_reingold_layout(graph1, center=(2, 2), scale=0.3)
        positions2 = drawing.layout.fruchterman_reingold_layout(graph2, center=(-1, 2), scale=4)
        positions3 = drawing.layout.fruchterman_reingold_layout(graph3, center=(-2, -2), scale=1.5)
        positions4 = drawing.layout.fruchterman_reingold_layout(graph4, center=(-4, 2), scale=1.5)
        positions5 = drawing.layout.fruchterman_reingold_layout(graph5, center=(2, -2), scale=0.25)
        positions = {**positions1, **positions2, **positions3, **positions4, **positions5}
        graph = compose_all([graph1, graph2, graph3, graph4, graph5])
    else:
        graph = tmp_graph

    graph.add_edges_from(list(tmp_graph.edges))

    # Placeholder that could let you add links manually to some unscrappable devices
    #graph.add_edge("unscrappable_device1", "unscrappable_device2)

    return graph, positions

def create_frontend_figure(graph, positions):

    set_node_attributes(graph, positions, "pos")

    edge_trace = graph_objs.Scatter(
        x=[], y=[], text=[], line=dict(width=0.5, color="#888"), hoverinfo="text", mode="lines+markers+text"
    )
    for edge in graph.edges():
        try:
            x0, y0 = graph.nodes[edge[0]]["pos"]
        except KeyError:
            print(f"keyError for {edge}")
        try:
            x1, y1 = graph.nodes[edge[1]]["pos"]
        except KeyError:
            print(f"keyError for {edge}")

        edge_trace["x"] += tuple([x0, x1, None])
        edge_trace["y"] += tuple([y0, y1, None])
        infos = str(edge)
        edge_trace["text"] += tuple([infos])

    node_marker = dict(
        showscale=False,
        colorscale="YlGnBu",
        reversescale=True,
        color=[],
        size=2,
        colorbar=dict(thickness=15, title="Node connections", xanchor="left", titleside="right"),
        line=dict(width=1),
    )

    node_trace = graph_objs.Scatter(
        x=[],
        y=[],
        text=[],
        name="Edges",
        mode="markers+text",
        marker=node_marker,
        hoverinfo="text",
        textfont=dict(color="#82d989", size=[]),
        textposition="bottom center",
    )
    for node, data in graph.nodes.data():
        try:
            x, y = graph.nodes[node]["pos"]
            node_trace["x"] += tuple([x])
            node_trace["y"] += tuple([y])
            infos = node + " " + str(data)
            node_trace["text"] += tuple([infos])
        except KeyError:
            print(f"keyError again for {node}")

    figure = graph_objs.Figure(
        data=[edge_trace, node_trace],
        layout=graph_objs.Layout(
            title="Scrapped_devices",
            titlefont=dict(size=16),
            showlegend=False,
            hovermode="closest",
            margin=dict(b=15, l=10, r=10, t=30),
            annotations=[
                dict(
                    text="made by you",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.005,
                    y=-0.002,
                )
            ],
            xaxis=graph_objs.layout.XAxis(showgrid=False, zeroline=False, showticklabels=True),
            yaxis=graph_objs.layout.YAxis(showgrid=False, zeroline=False, showticklabels=True),
        ),
    )

    return figure


def drawing_advanced(formatted_results, multigraphs=True):

    # Fixed positions for the central nodes
    # fixed_pos = {}

    graph, positions = create_frontend_graph(formatted_results, multigraphs)

    figure = create_frontend_figure(graph, positions)

    try:
        plotly.iplot(figure, filename="graph.html")
    except:
        plot(figure, filename="graph.html")

def main() -> None:
    """ Retrieve the results of scrapping from a file 
    and draws a graph from them """

    with open("lldp_scrapping_results", "r") as res:
        formatted_results = literal_eval(res.read())

    print("\n\nGenerating the Graph, please wait.\n\n")

    drawing_advanced(formatted_results)


if '__main__' in __name__:
    main()
