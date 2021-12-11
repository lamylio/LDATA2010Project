from pyvis.network import Network
from app import * 
from requirements import *
from storage import *

import networkx as nx

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
    Output("net_card", "style"),
    Output("network", "srcDoc"),
    Output("loading_configurator", "children"),
    Output("alert_configurator", "is_open"),

    Input(store_id, "data"),
    Input(store_settings, "data"),
)
def update_graph(session_id, new_settings):
    if app.server.debug: print(session_id, "> update_graph > start")
    if new_settings == None: raise PreventUpdate

    try:
        # RETRIEVE
        graph = get_graph(session_id)
        settings = get_settings(session_id)
        df_nodes = get_dataframe(session_id, "nodes")
        df_edges = get_dataframe(session_id, "edges")

        # NODES CREATION
        if settings.get("COL_NODES_ID") != new_settings.get("COL_NODES_ID"):
            if not df_nodes.empty and new_settings.get("COL_NODES_ID") != None: 
                if app.server.debug: print(session_id, "> update_graph > update nodes")
                graph.clear()
                graph.add_nodes_from(populate_nodes(df_nodes, new_settings.get("COL_NODES_ID")))

        # EDGES CREATION
        if  settings.get("COL_EDGES_FROM") != new_settings.get("COL_EDGES_FROM") or \
            settings.get("COL_EDGES_TO") != new_settings.get("COL_EDGES_TO") or \
            settings.get("COL_NODES_ID") != new_settings.get("COL_NODES_ID"):
            
            if not df_edges.empty and new_settings.get("COL_EDGES_FROM") != None and new_settings.get("COL_EDGES_TO") != None:
                if app.server.debug: print(session_id, "> update_graph > update edges")
                graph.clear_edges()
                graph.add_edges_from(populate_edges(df_edges, new_settings.get("COL_EDGES_FROM"), new_settings.get("COL_EDGES_TO"), graph.nodes))

        
        # SAVE
        save_settings(session_id, new_settings)
        save_graph(session_id, graph)

        # IF EMPTY
        if nx.number_of_nodes(graph) < 1: return ({}, no_update, html.Div(), False)

        # LAYOUT
        layout = nx.circular_layout(graph) # TODO: use configuration
        pos_nodes = {id: {"x": pos[0]*500, "y": pos[1]*500} for id, pos in layout.items()} 
        nx.set_node_attributes(graph, pos_nodes)

        # NETWORK
        net = Network("1000px", "100%")
        net.from_nx(graph, default_node_size=5, default_edge_weight=1)
        net.toggle_physics(False)

        # OPTIONS OF NODES
        neighbors_list = net.get_adj_list()
        for node in net.nodes:        
            # LABELS
            if new_settings.get("SHOW_NODES_LABELS") == False: node['label'] = ""
            else:
                if new_settings.get("COL_NODES_LABEL") != None: 
                    df_labels = isolate_by_id(df_nodes, new_settings.get("COL_NODES_ID"), new_settings.get("COL_NODES_LABEL"))
                    node['label'] = df_labels.loc[node['id']][0]
                else:
                    node['label'] = node['id']

            # TITLE
            if net.num_edges() > 0:
                nb = neighbors_list[node['id']]
                nb_li = "<br>".join([str(
                    net.get_node(n).get(("id","label")[new_settings.get("SHOW_NODES_LABELS")])
                ) for n in nb])
                node['title'] = f"Neighbors of {node['label']}: <br>" + ("There is none :(", nb_li)[len(nb) > 0]

            # SIZE
            if new_settings.get("COL_NODES_SIZE") != None:
                if new_settings.get("COL_NODES_SIZE") == "@NEIGHBORS":
                    node['value'] = len(neighbors_list[node['id']])
                else:
                    df_size = isolate_by_id(df_nodes, new_settings.get("COL_NODES_ID"), new_settings.get("COL_NODES_SIZE"))
                    node['value'] = df_size.loc[node['id']][0]

        # OUTPUT
        net.write_html(f"networks/{session_id}.html")
    except: return (no_update, no_update, html.Div(), True)
    # EVERYTHING IS OK
    if app.server.debug: print(session_id, "> update_graph > draw graph")
    return ({"display": "none"}, net.html, html.Div(), False)


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
    

