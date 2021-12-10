from pyvis.network import Network
from app import * 
from requirements import *
from storage import *

import networkx as nx
from networkx import number_of_nodes, number_of_edges

@cache.memoize()
def populate_nodes(df, column):
    return df[column].drop_duplicates().dropna()

@cache.memoize()
def populate_edges(df, col_from, col_to, nodes):
    dfc = df[[col_from, col_to]].drop_duplicates()
    edges_clean = [(fr, to) for fr, to in zip(
        dfc[col_from],
        dfc[col_to]
    ) if fr in nodes and to in nodes]
    return edges_clean

@cache.memoize()
def from_nx_to_net(graph):
    pass

@app.callback(
    Output("net_card", "style"),
    Output("network", "srcDoc"),

    Input(store_id, "data"),
    Input(store_settings, "data"),
)
def update_graph(session_id, new_settings):
    if app.server.debug: print(session_id, "> update_graph > start")
    if new_settings == None: raise PreventUpdate

    # Update

    graph = get_graph(session_id)
    settings = get_settings(session_id)
    df_nodes = get_dataframe(session_id, "nodes")
    df_edges = get_dataframe(session_id, "edges")

    print(settings)
    print(new_settings)
    print(df_nodes.empty, df_edges.empty)
    print(get_dataframe(session_id, "nodes").size)
    # Node ID update
    if settings.get("COL_NODES_ID") != new_settings.get("COL_NODES_ID"):
        if not df_nodes.empty and new_settings.get("COL_NODES_ID") != None: 
            if app.server.debug: print(session_id, "> update_graph > update nodes")
            graph.clear()
            graph.add_nodes_from(populate_nodes(df_nodes, new_settings.get("COL_NODES_ID")))

    # Edges update
    if  settings.get("COL_EDGES_FROM") != new_settings.get("COL_EDGES_FROM") or \
        settings.get("COL_EDGES_TO") != new_settings.get("COL_EDGES_TO") or \
        settings.get("COL_NODES_ID") != new_settings.get("COL_NODES_ID"):
        
        if not df_edges.empty and new_settings.get("COL_EDGES_FROM") != None and new_settings.get("COL_EDGES_TO") != None:
            if app.server.debug: print(session_id, "> update_graph > update edges")
            graph.clear_edges()
            graph.add_edges_from(populate_edges(df_edges, new_settings.get("COL_EDGES_FROM"), new_settings.get("COL_EDGES_TO"), graph.nodes))

    if app.server.debug: print(session_id, "> update_graph > save settings")
    save_settings(session_id, new_settings)

    if nx.number_of_nodes(graph) < 1: return ({}, no_update)
    if app.server.debug: print(session_id, "> update_graph > layout creation")

    layout = nx.circular_layout(graph) # TODO: use configuration
    pos_nodes = {id: {"fixed": {"x": True, "y": True}, "x": pos[0]*500, "y": pos[1]*500} for id, pos in layout.items()} # "title": "\n".join(graph.neighbors(str(id)))
    nx.set_node_attributes(graph, pos_nodes)
    
    if app.server.debug: print(session_id, "> update_graph > save graph")
    save_graph(session_id, graph)

    if app.server.debug: print(session_id, "> update_graph > from nx to network")
    net = Network("1000px", "100%")
    net.from_nx(graph, default_node_size=5, default_edge_weight=1)
    # net.toggle_physics(False)
    net.write_html(f"networks/{session_id}.html")
    if app.server.debug: print(session_id, "> update_graph > draw graph")
    return ({"display": "none"}, net.html)


# @app.callback(
#     Output("net_card", "style"),
#     Output("network", "srcDoc"),
#     State(store_id, "data"),
#     Input(store_graph, "data")
# )
# def draw_graph_from_local(session_id, local_graph):
#     if not dataframe_exists(session_id, "nodes"): return ({}, no_update)
#     if not local_graph: return ({}, no_update)
#     if app.server.debug: print("draw_graph > start")
#     graph = nx.node_link_graph(local_graph)
#     if app.server.debug: print("draw_graph > layout (circular)")
#     layout = nx.circular_layout(graph)
#     pos_nodes = {id: {"x": pos[0], "y": pos[1], "title": "\n".join(graph.neighbors(str(id)))} for id, pos in layout.items()}
#     nx.set_node_attributes(graph, pos_nodes)
#     if app.server.debug: print("draw_graph > network")
#     net = Network("1000px", "100%")
#     net.from_nx(graph)
#     net.write_html(f"networks/{session_id}.html")
#     if app.server.debug: print("draw_graph > end")
#     return ({"display": "none"}, net.html)
    

