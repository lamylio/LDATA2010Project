from networkx.classes.function import neighbors
from pyvis.network import Network
from app import * 
from requirements import *
from storage import *

import networkx as nx
from math import log2

from utils import layout_value_to_function

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
def isolate_by_id(df, column_id, column_to_isolate):
    return df[[column_id, column_to_isolate]].set_index(column_id)

@app.callback(
    dict(
        style=Output("net_card", "style"),
        network=Output("network", "srcDoc"),
        loading=Output("loading_configurator", "children"),
        alert=Output("alert_configurator", "is_open"),
    ),
    Input(store_id, "data"),
    Input(store_settings, "data"),
)
def update_graph(session_id, settings):
    if app.server.debug: print(session_id, "> update_graph > start")
    if settings == None: raise PreventUpdate

    try:
        # RETRIEVE
        graph = get_graph(session_id)
        session_settings = get_settings(session_id)
        df_nodes = get_dataframe(session_id, "nodes")
        df_edges = get_dataframe(session_id, "edges")

        # NODES CREATION
        if session_settings.get("COL_NODES_ID") != settings.get("COL_NODES_ID"):
            if not df_nodes.empty and settings.get("COL_NODES_ID") != None: 
                if app.server.debug: print(session_id, "> update_graph > update nodes")
                graph.clear()
                graph.add_nodes_from(populate_nodes(df_nodes, settings.get("COL_NODES_ID")))

        # EDGES CREATION
        if  session_settings.get("COL_EDGES_FROM") != settings.get("COL_EDGES_FROM") or \
            session_settings.get("COL_EDGES_TO") != settings.get("COL_EDGES_TO") or \
            session_settings.get("COL_NODES_ID") != settings.get("COL_NODES_ID"):
            
            if not df_edges.empty and settings.get("COL_EDGES_FROM") != None and settings.get("COL_EDGES_TO") != None:
                if app.server.debug: print(session_id, "> update_graph > update edges")
                graph.clear_edges()
                graph.add_edges_from(populate_edges(df_edges, settings.get("COL_EDGES_FROM"), settings.get("COL_EDGES_TO"), graph.nodes))

        
        # SAVE
        save_settings(session_id, settings)
        save_graph(session_id, graph)

        # IF EMPTY STOP HERE
        if nx.number_of_nodes(graph) < 1: return dict(style={}, network=no_update, loading=html.Div(), alert=False)

        # OTHERWISE
        if settings.get("COL_NODES_LABEL") != None: 
            df_labels = isolate_by_id(df_nodes, settings.get("COL_NODES_ID"), settings.get("COL_NODES_LABEL"))
            def get_label(node_id):
                if settings.get("SHOW_NODES_LABELS") != False: return str(df_labels.loc[node_id][0])
                return ""

        if settings.get("COL_NODES_SIZE") not in [None, "@NEIGHBORS"]: 
            df_size = isolate_by_id(df_nodes, settings.get("COL_NODES_ID"), settings.get("COL_NODES_SIZE"))
            def get_size(node_id):
                return 5+log2(1+abs(float(df_size.loc[node_id][0])))          

        # LAYOUT
        if app.server.debug: print(session_id, "> update_graph > define layout")
        layout_fn = layout_value_to_function(settings.get("GRAPH_LAYOUT"))
        if layout_fn != None:
            layout = layout_fn(graph)
            expansion = 1000
            pos_nodes = {
                id: {
                    "x": pos[0]*expansion, "y": pos[1]*expansion
                } for id, pos in layout.items()} 
            nx.set_node_attributes(graph, pos_nodes)

        graph.nodes[121087]["custom_color"] = "#00ff00"

        # TO NETWORK
        if app.server.debug: print(session_id, "> update_graph > to network")
        net = Network("1000px", "100%")
        net.from_nx(graph, default_node_size=5, default_edge_weight=1, )
        net.toggle_physics(layout_fn == None)

        # NODES ATTRIBUTES ADJUSTMENTS
        if app.server.debug: print(session_id, "> update_graph > nodes attributes")
        nodes_neighbors = net.get_adj_list()
        for node in net.nodes:
            # LABEL
            if app.server.debug: print(session_id, "> update_graph > nodes attributes > label")
            if settings.get("COL_NODES_LABEL") != None: node["label"] = get_label(node['id'])
            else: node["label"] = ("", node['id'])[settings.get("SHOW_NODES_LABELS") != False]
            # TITLE
            if app.server.debug: print(session_id, "> update_graph > nodes attributes > title")
            node["title"] = f"{node['id']} has {len(nodes_neighbors.get(node['id']))} neighbors"
            # COLOR
            if app.server.debug: print(session_id, "> update_graph > nodes attributes > color")
            if node.get('custom_color') != None: node['color'] = node['custom_color']
            else: node['color'] = settings.get("GLOBAL_NODES_COLOR")
            # SIZE
            if app.server.debug: print(session_id, "> update_graph > nodes attributes > size")
            if settings.get("COL_NODES_SIZE") != None and len(nodes_neighbors[node['id']]) > 0:
                if settings.get("COL_NODES_SIZE") !="@NEIGHBORS": node["size"] = get_size(node['id'])
                else : node["size"] = float(len(nodes_neighbors[node['id']])) / 2

        # OUTPUT
        if app.server.debug: print(session_id, "> update_graph > output")
        net.write_html(f"networks/{session_id}.html")
    except Exception as e: 
        print(e)
        return dict(style=no_update, network=no_update, loading=html.Div(), alert=True)
    # EVERYTHING IS OK
    if app.server.debug: print(session_id, "> update_graph > draw graph")
    return dict(style={"display": "none"}, network=net.html, loading=html.Div(), alert=False)
    

