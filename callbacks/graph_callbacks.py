from app import * 
from requirements import *
from storage import *

import networkx as nx
from utils import (
    layout_value_to_function, 
    graph_alert_message, 
    populate_nodes, populate_edges,
    constrasting_text, hex_to_rgba
)


@app.callback(
    dict(
        network=Output("network", "data"),
        network_options=Output("network", "options"),
        card_no_data=Output("card_no_data", "className"),
        loading=Output("loading_configurator", "children"),
        alert=Output("alert_configurator", "is_open"),
        alert_message=Output("alert_configurator", "children")
    ),
    Input(store_id, "data"),
    Input(store_settings, "data"),
)
def update_graph(session_id, settings):
    if app.server.debug: print(session_id, "> update_graph > start")
    if settings == None: raise PreventUpdate

    def has_changed(setting):
        return session_settings.get(setting) != settings.get(setting)
        
    def is_set(setting):
        return settings.get(setting, None) not in [None, "@NONE"]

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
        if nx.number_of_nodes(graph) < 1: return dict(
            alert=graph_exists(session_id), alert_message=graph_alert_message("No nodes found.."),
            network=no_update, network_options=no_update,
            card_no_data=no_update, loading=html.Div() 
        )
        if app.server.debug: print(session_id, "> update_graph > graph is not empty")
                
        if is_set("COL_NODES_LABEL"): 
            if app.server.debug: print(session_id, "> update_graph > obtain labels")
            df_nodes_label = df_nodes[[COL_NODES_ID, COL_NODES_LABEL]].groupby([COL_NODES_ID])

        if is_set("COL_NODES_SIZE"): 
            if app.server.debug: print(session_id, "> update_graph > obtain nodes sizes")
            df_nodes_size = df_nodes[[COL_NODES_ID, COL_NODES_SIZE]].groupby([COL_NODES_ID])

        if is_set("COL_EDGES_WEIGHT"):
            if app.server.debug: print(session_id, "> update_graph > obtain edges weights")
            df_edges_weight = df_edges[[COL_EDGES_FROM, COL_EDGES_TO, COL_EDGES_WEIGHT]].groupby([COL_EDGES_FROM, COL_EDGES_TO])

        # LAYOUT
        if app.server.debug: print(session_id, "> update_graph > define layout")
        layout_fn = layout_value_to_function(settings.get("GRAPH_LAYOUT"))
        layout = layout_fn(graph)
        scale=500

        def get_label(id):
            if settings.get("SHOW_NODES_LABELS", False) == False: return None
            if is_set("COL_NODES_LABEL"): return df_nodes_label.get_group(id).values[0][-1]
            return str(id)

        # SET GRAPH ATTRIBUTES
        if app.server.debug: print(session_id, "> update_graph > nx_nodes")
        nx_nodes = {id: {
            "x": pos[0]*scale, "y": pos[1]*scale,
            "value":  df_nodes_size.get_group(id).values[0][-1] or 5 if is_set("COL_NODES_SIZE") else 5,
            "size":  df_nodes_size.get_group(id).values[0][-1] or 5 if is_set("COL_NODES_SIZE") else 5,
            "label": get_label(id)
        } for id, pos in layout.items()}
        
        if app.server.debug: print(session_id, "> update_graph > nx_edges")
        nx_edges = {
            (efrom, eto): {
                "value": df_edges_weight.get_group((efrom, eto)).values[0][-1] if is_set("COL_EDGES_WEIGHT") else 1,
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
            "color": hex_to_rgba(settings.get('NODES_COLOR', '#000000'), int(settings.get('NODES_OPACITY', 100))/100),
            "fixed": False,
            "font": {
                "color": "#000000", # constrasting_text(hex_to_rgba(settings.get('NODES_COLOR', '#000000'), int(settings.get('NODES_OPACITY', 100))/100))
            },
            "shape": "dot",
            "scaling": {
                "min": 5,
                "max": 15,
                "label": {
                    "enabled": True,
                    "min": 5,
                    "max": 15
                }
            }
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
            "color": settings.get('EDGES_COLOR', '#000000'),

            "font": {
                "size": 11
            },
            "scaling": {
                "min": 1,
                "max": 15,
            }
        }
        
        if app.server.debug: print(session_id, "> update_graph > to network > net_options_interactions")
        net_options_interactions = {
            "keyboard": True,
            "multiselect": False,
            "navigationButtons": True
        }
        
        if app.server.debug: print(session_id, "> update_graph > to network > net_options_physics")
        net_options_physics = {
            "stabilization": False,
            "timestep": 0,
            "adaptiveTimestep": False
        }
        
        if app.server.debug: print(session_id, "> update_graph > to network > net_options_manipulation")
        net_options_manipulation = {
            "enabled": True
        }
        
        net_options = {
            "height": "100%",
            "width":  "100%",
            "edges": net_options_edges,
            "nodes": net_options_nodes,
            "interaction": net_options_interactions,
            "manipulation": net_options_manipulation,
            "physics": net_options_physics
        }
        
        if app.server.debug: print(session_id, "> update_graph > return graph")
        return dict(
            alert=False, alert_message=no_update,
            network=net_data, network_options=net_options,
            card_no_data="d-none", loading=html.Div() 
        )
    
        # NODES ATTRIBUTES ADJUSTMENTS
        # TODO ? 
        
    except Exception as e: 
        print(e)
        return dict(
            alert=True, alert_message=graph_alert_message(str(e.args)),
            network=no_update, network_options=no_update,
            card_no_data=no_update, loading=html.Div()
        )    



@app.callback(
    dict(
        title=Output("card_selected_node_header", "children"),
        body=Output("card_selected_node_body", "children"),
    ),
    Input("network", "selection"),
    Input("network", "data")
)
def get_selected_nodes(selection, data):
    if not selection: raise PreventUpdate
    nodes = selection.get("nodes", [])
    if len(nodes) < 1: raise PreventUpdate
    node_id = nodes[0]

    attrs = [n for n in data.get("nodes") if n["id"] == node_id][0].items()
    attrs_body = [[f"{k}: {v}", html.Br()] for k,v in attrs]
    attrs_body_joined = [child for list in attrs_body for child in list]
    return dict(title=node_id, body=attrs_body_joined)
