from networkx.algorithms.centrality.betweenness import betweenness_centrality
from app import * 
from requirements import *
from storage import *
from utils import *

from .graph_callbacks_options import get_all_options
import networkx as nx


@app.callback(
    dict(
        store_network=Output("store_network", "data"),
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
        
        COL_EDGES_ID = settings.get("COL_EDGES_ID")
        COL_EDGES_FROM = settings.get("COL_EDGES_FROM")
        COL_EDGES_TO = settings.get("COL_EDGES_TO")
        COL_EDGES_WEIGHT = settings.get("COL_EDGES_WEIGHT")

        COL_FOCUS_ON = settings.get("COL_FOCUS_ON")
        COL_FOCUS_VALUE = settings.get("COL_FOCUS_VALUE") or "@NONE"

        # NODES CREATION
        if is_set("COL_NODES_ID"):
            if app.server.debug: print(session_id, "> update_graph > set nodes index")
            if not dataframe_exists(session_id, "nodes"): raise Exception("The nodes dataframe is empty..")
            df_nodes = df_nodes.set_index(COL_NODES_ID)

            if not df_nodes.empty: 
                if app.server.debug: print(session_id, "> update_graph > update nodes")
                graph.clear()
                graph.add_nodes_from(df_nodes.index)

        # EDGES CREATION

        if is_set("COL_EDGES_ID"):
            if app.server.debug: print(session_id, "> update_graph > set edges index")
            df_edges = df_edges.set_index(COL_EDGES_ID)

        if is_set("COL_NODES_ID") and is_set("COL_EDGES_FROM") and is_set("COL_EDGES_TO") and not df_edges.empty:
            if app.server.debug: print(session_id, "> update_graph > update edges")
            populated_edges = populate_edges(df_edges, COL_EDGES_FROM, COL_EDGES_TO, graph.nodes())
            graph.remove_edges_from(graph.edges())
            graph.add_edges_from(populated_edges)


        # IF EMPTY STOP HERE
        if nx.number_of_nodes(graph) < 1: return dict(
            alert=graph_exists(session_id), alert_message=graph_alert_message("No nodes found.."),
            store_network=no_update,
            loading=html.Div() 
        )
        if app.server.debug: print(session_id, "> update_graph > graph is not empty")
                
        # DERIVATED DATAFRAMES
        if is_set("COL_NODES_LABEL"): 
            if app.server.debug: print(session_id, "> update_graph > obtain labels")
            # df_nodes_label = df_nodes[[COL_NODES_ID, COL_NODES_LABEL]].groupby([COL_NODES_ID])
            df_nodes_label = df_nodes[COL_NODES_LABEL]

        if is_set("COL_NODES_SIZE"): 
            if app.server.debug: print(session_id, "> update_graph > obtain nodes sizes")
            # df_nodes_size = df_nodes[[COL_NODES_ID, COL_NODES_SIZE]].groupby([COL_NODES_ID])
            df_nodes_size = df_nodes[COL_NODES_SIZE]

        if is_set("COL_EDGES_WEIGHT"):
            if app.server.debug: print(session_id, "> update_graph > obtain edges weights")
            df_edges_weight = df_edges[COL_EDGES_WEIGHT]

        if is_set("COL_FOCUS_ON"):
            # df_focus = df_nodes[[COL_NODES_ID, COL_FOCUS_ON]].groupby([COL_NODES_ID])
            df_focus = df_nodes[COL_FOCUS_ON]

        def get_label(id):
            if settings.get("SHOW_NODES_LABELS", False) == False: return None
            if is_set("COL_NODES_LABEL"): return get_value_matching_index(df_nodes_label, id)
            return str(id)

        # SET GRAPH ATTRIBUTES
        if app.server.debug: print(session_id, "> update_graph > nx_nodes")
        ## Create nx_nodes
        nx_nodes = {
            id: {
                "value":  get_value_matching_index(df_nodes_size, id, 0) if is_set("COL_NODES_SIZE") else 0,
                "focus":  str(get_value_matching_index(df_focus, id)) if is_set("COL_FOCUS_ON") else None,
                **({"group": "@NOT_FOCUS"},{})[is_set("COL_FOCUS_ON")],
                "label": get_label(id)
            } for id in graph.nodes()
        }

        ## Keep only focus group
        if is_set("COL_FOCUS_ON") and is_set("COL_FOCUS_VALUE"):
            if app.server.debug: print(session_id, "> update_graph > nx_nodes > keep focus")
            focus_nodes_id = [id for id,options in nx_nodes.items() if options.get("focus") == COL_FOCUS_VALUE]
            focus_nodes_neigh = {neigh_id for node_id in focus_nodes_id for neigh_id in graph.neighbors(node_id)}
            focus_nodes_to_keep = set(focus_nodes_id).union(focus_nodes_neigh)
            nx_nodes = {id: {"group" : ("@NOT_FOCUS", COL_FOCUS_VALUE)[options.get("focus") == COL_FOCUS_VALUE], **options} for id,options in nx_nodes.items() if id in focus_nodes_to_keep}
            graph.remove_nodes_from([id for id in graph.nodes() if id not in focus_nodes_to_keep])

        ## Set nodes layout and position
        if app.server.debug: print(session_id, "> update_graph > nx_nodes > layout")
        layout_fn, layout_args = layout_value_to_function(settings.get("GRAPH_LAYOUT"))
        layout = layout_fn(graph, **layout_args)
        pos = {
            id: {
                "x": pos[0], "y": pos[1]
            } for id, pos in layout.items()
        }
        nx_nodes = {
            id: {
                **pos[id],
                **options
            } for id, options in nx_nodes.items()
        }
        
        ## Create nx_edges
        if app.server.debug: print(session_id, "> update_graph > nx_edges")
        nx_edges = {
            (u, v): {
                "value": get_value_matching_index(df_edges_weight, e_options["id"], 1) if is_set("COL_EDGES_WEIGHT") else 1,
                "label": e_options.get("id", "") if is_set("COL_EDGES_ID") else None,
                **e_options
            } for u, v, e_options in graph.edges(data=True) if u in nx_nodes.keys() and v in nx_nodes.keys()
        }

        ## update graph with nodes and edges attributes
        if app.server.debug: print(session_id, "> update_graph > nx set attributes")
        nx.set_node_attributes(graph, nx_nodes)
        nx.set_edge_attributes(graph, nx_edges)

        # SAVE
        if app.server.debug: print(session_id, "> update_graph > save graph and settings")
        save_settings(session_id, settings)
        save_graph(session_id, graph)

        # TO NETWORK
        if app.server.debug: print(session_id, "> update_graph > to network")
        ## net_nodes mapping
        if app.server.debug: print(session_id, "> update_graph > to network > net_nodes")
        net_nodes = [{
            "id": id, 
            **n_options
        } for id, n_options in nx_nodes.items()]
        
        ## net_edges mapping
        if app.server.debug: print(session_id, "> update_graph > to network > net_edges")
        net_edges = [{
            "from": u, 
            "to": v, 
            **e_options
        } for u, v, e_options in graph.edges(data=True, default={})]

        net_data = {"nodes": net_nodes, "edges": net_edges}
        
        ## network options
        net_options = get_all_options(session_id, settings)
        
        # RETURN
        if app.server.debug: print(session_id, "> update_graph > return graph")
        return dict(
            alert=False, alert_message=no_update,
            store_network={"data": net_data, "options": net_options},
            loading=html.Div() 
        )

    except Exception as e: 
        print(e)
        return dict(
            alert=True, alert_message=graph_alert_message(str(e.args[0])),
            store_network=no_update,
            loading=html.Div()
        )    


# SHOW SELECTION 
@app.callback(
    dict(
        title=Output("card_selected_node_header", "children"),
        body=Output("card_selected_node_body", "children"),
    ),
    State(store_id, "data"),
    Input("network", "selection"),
    Input("show_selected_node_switch", "value"),
)
def get_selected_nodes(session_id, selection, switch):
    if not switch or not selection or not graph_exists(session_id): raise PreventUpdate
    nodes = selection.get("nodes", [])
    if len(nodes) < 1: raise PreventUpdate
    
    node_id = nodes[0]
    graph = get_graph(session_id)
    nx_node = graph.nodes.get(node_id)
    node_label = nx_node.get("label")

    # Title 
    title = f"{node_label} ({node_id})"
    
    # Body

    graph_betweenness_centrality = nx.betweenness_centrality(graph)
    node_clustering_coeff = nx.clustering(graph, node_id)
    infos = {
        "Size": nx_node.get("value"),
        "Group": nx_node.get("group")
    }

    metrics = {
        "Degree": round(graph.degree[node_id], 2),
        "Betweness centrality": round(graph_betweenness_centrality.get(node_id),2),
        "Clustering coeff": round(node_clustering_coeff,2),

    }

    body = [html.P(f"{k}: {v}") for k,v in infos.items()] + [html.Hr()] + [html.P(f"{k}: {v}")for k,v in metrics.items()]
    return dict(title=title, body=body)
