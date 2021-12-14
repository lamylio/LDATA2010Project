from networkx.classes.function import neighbors
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
        network=Output("network", "data"),
        network_options=Output("network", "options"),
        card_no_data=Output("card_no_data", "className"),
        loading=Output("loading_configurator", "children"),
        alert=Output("alert_configurator", "is_open"),
    ),
    Input(store_id, "data"),
    Input(store_settings, "data"),
)
def update_graph(session_id, settings):
    if app.server.debug: print(session_id, "> update_graph > start")
    if settings == None: return dict(card_no_data=no_update, network=no_update, network_options=no_update, loading=html.Div(), alert=no_update)

    try:
        # RETRIEVE
        if app.server.debug: print(session_id, "> update_graph > retrieve data")
        graph = get_graph(session_id)
        session_settings = get_settings(session_id)
        df_nodes = get_dataframe(session_id, "nodes")
        df_edges = get_dataframe(session_id, "edges")
        
        COL_NODES_ID = settings.get("COL_NODES_ID")
        COL_NODES_LABEL = settings.get("COL_NODES_LABEL")
        COL_NODES_SIZE = settings.get("COL_NODES_SIZE")
        
        COL_EDGES_FROM = settings.get("COL_EDGES_FROM")
        COL_EDGES_TO = settings.get("COL_EDGES_TO")
        COL_EDGES_WEIGHT = settings.get("COL_EDGES_WEIGHT")
                
        def has_changed(setting):
            return session_settings.get(setting) != settings.get(setting)
        
        def is_set(setting):
            return settings.get(setting, None) != None

        # NODES CREATION
        if has_changed("COL_NODES_ID"):
            if not df_nodes.empty and COL_NODES_ID != None: 
                if app.server.debug: print(session_id, "> update_graph > update nodes")
                graph.clear()
                graph.add_nodes_from(populate_nodes(df_nodes, COL_NODES_ID))

        # EDGES CREATION
        if has_changed("COL_EDGES_FROM") or has_changed("COL_EDGES_TO") or has_changed("COL_NODES_ID"):
            if not df_edges.empty and COL_EDGES_FROM != None and COL_EDGES_TO != None:
                if app.server.debug: print(session_id, "> update_graph > update edges")
                populated_edges = populate_edges(df_edges, COL_EDGES_FROM, COL_EDGES_TO, graph.nodes)
                graph.remove_edges_from(dict(graph.edges))
                graph.add_edges_from(populated_edges)


        # IF EMPTY STOP HERE
        if nx.number_of_nodes(graph) < 1: return dict(card_no_data="", network=no_update, network_options=no_update, loading=html.Div(), alert=False)
        if app.server.debug: print(session_id, "> update_graph > graph is not empty")
                
        if is_set("COL_NODES_LABEL"): 
            if app.server.debug: print(session_id, "> update_graph > obtain labels")
            df_labels = isolate_by_id(df_nodes, COL_NODES_ID, COL_NODES_LABEL)

        if settings.get("COL_NODES_SIZE") not in [None, "@NONE", "@NEIGHBORS"]: 
            if app.server.debug: print(session_id, "> update_graph > obtain nodes sizes")
            df_nodes_size = isolate_by_id(df_nodes, COL_NODES_ID, COL_NODES_SIZE)   

        if is_set("COL_EDGES_WEIGHT"):
            if app.server.debug: print(session_id, "> update_graph > obtain edges weights")
            df_edges_weight = df_edges[[COL_EDGES_FROM, COL_EDGES_TO, COL_EDGES_WEIGHT]].groupby([COL_EDGES_FROM, COL_EDGES_TO])

        # LAYOUT
        if app.server.debug: print(session_id, "> update_graph > define layout")
        layout_fn = layout_value_to_function(settings.get("GRAPH_LAYOUT"))
        if layout_fn == None: return dict(card_no_data="d-none", network=no_update, network_options=no_update, loading=html.Div(), alert=True)
        layout = layout_fn(graph)
        expansion = 1000
        
        # SET GRAPH ATTRIBUTES
        if app.server.debug: print(session_id, "> update_graph > nx_nodes")
        nx_nodes = {id: {
            "x": pos[0]*expansion, "y": pos[1]*expansion,
            "value":  df_nodes_size.loc[id][0] if settings.get("COL_NODES_SIZE") not in [None, "@NONE", "@NEIGHBORS"] else None
        } for id, pos in layout.items()}
        
        if app.server.debug: print(session_id, "> update_graph > nx_edges")
        nx_edges = {
            (efrom, eto): {
                "value": df_edges_weight.get_group((efrom, eto))[COL_EDGES_WEIGHT][0] if is_set("COL_EDGES_WEIGHT") else None
            } for efrom, eto in graph.edges()
        }
        if app.server.debug: print(session_id, "> update_graph > nx set attributes")
        nx.set_node_attributes(graph, nx_nodes)
        nx.set_edge_attributes(graph, nx_edges)
        
        # SAVE
        if app.server.debug: print(session_id, "> update_graph > save graph and settings")
        save_settings(session_id, settings)
        save_graph(session_id, graph)

        # TO NETWORK
        if app.server.debug: print(session_id, "> update_graph > to network")
        if app.server.debug: print(session_id, "> update_graph > to network > net_nodes")
        net_nodes = [{
            "id": id, 
            **n_options
        } for id, n_options in graph.nodes(data=True, default={})]

        net_nodes[0]["color"] = "#00ff00" # TEST
        
        if app.server.debug: print(session_id, "> update_graph > to network > net_edges")
        net_edges = [{
            "id": f"{u}-{v}", 
            "from": u, 
            "to": v, 
            **e_options
        } for u, v, e_options in graph.edges(data=True, default={})]
        
        net_data = {
            "nodes": net_nodes,
            "edges": net_edges        
        }
        
        if app.server.debug: print(session_id, "> update_graph > to network > net_options_nodes")
        net_options_nodes = {
            "color": settings.get("NODES_COLOR", "#000000"),
            "opacity": int(settings.get("NODES_OPACITY", 100))/100,
            "fixed": {
                "x": "x" in settings.get("FIXED_X_Y", []) or False,
                "y": "y" in settings.get("FIXED_X_Y", []) or False
            },
            "font": {
                "size": 11
            },
        }
        
        if app.server.debug: print(session_id, "> update_graph > to network > net_options_edges")
        net_options_edges = {
            "arrows": {
                "from": {
                    "enabled": "from" in settings.get("EDGES_ARROWS", []) or False,
                    "scaleFactor": 1.1
                },
                "middle": {
                    "enabled": "middle" in settings.get("EDGES_ARROWS", []) or False,
                    "scaleFactor": 1.1
                },
                "to": {
                    "enabled": "to" in settings.get("EDGES_ARROWS", []) or False,
                    "scaleFactor": 1.1
                }
            },
            "arrowStrikethrough": False,
            "color": {
                "inherit": settings.get("EDGES_COLOR_INHERIT", True),
                "opacity": settings.get("EDGES_COLOR_OPACITY", 1)
            },
            "font": {
                "size": 11
            },
            "smooth": False
        }
        
        if app.server.debug: print(session_id, "> update_graph > to network > net_options_interactions")
        net_options_interactions = {
            "keyboard": True,
            "multiselect": True,
            "navigationButtons": True,
            "hideEdgesOnDrag": False,
            "hideEdgesOnZoom": False,
            "hideNodesOnDrag": False,
        }
        
        if app.server.debug: print(session_id, "> update_graph > to network > net_options_physics")
        net_options_physics = {
            "stabilization": {
                "onlyDynamicEdges": True
            }
        }
        
        net_options_manipulation = {
            "enabled": True,
            "addNode": False,
            "addEdge": False,
            "controlNodeStyle": net_options_nodes
        }
        
        net_options = {
            "height": "100%",
            "width":  "100%",
            "nodes": net_options_nodes,
            "edges": net_options_edges,
            "interactions": net_options_interactions,
            "physics": net_options_physics,
            "manipulation": net_options_manipulation
        }
        
        if app.server.debug: print(session_id, "> update_graph > return graph")
        return dict(card_no_data="d-none", network=net_data, network_options=net_options, loading=html.Div(), alert=False)
    
        # NODES ATTRIBUTES ADJUSTMENTS
        # TODO ? 
        
    except Exception as e: 
        print(e)
        return dict(card_no_data=no_update, network=no_update, network_options=no_update, loading=html.Div(), alert=True)
    

