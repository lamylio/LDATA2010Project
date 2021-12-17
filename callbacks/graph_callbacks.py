from networkx.algorithms.centrality.betweenness import betweenness_centrality
from app import * 
from requirements import *
from storage import *
from utils import *

from .graph_callbacks_options import get_all_options
import networkx as nx

from dash import callback_context


@app.callback(
    dict(
        network=Output(store_graph, "data"),
        loading=Output("loading_configurator", "children"),
        alert=Output("alert_configurator", "is_open"),
        alert_message=Output("alert_configurator", "children"),
        selection=Output("network", "selection")
    ),
    State(store_id, "data"),
    Input(store_settings, "data"),
    Input("network", "selection"),
)
def update_graph(session_id, settings, selection):
    if app.server.debug: print(session_id, "> update_graph > start")
    if settings == None: raise PreventUpdate()

    ctx = callback_context
    ctx_id = ctx.triggered[0]['prop_id'].split(".")[0]

    if ctx_id == "network":
        if not selection: raise PreventUpdate()
        if len(selection.get("nodes", [])) != 2: raise PreventUpdate()
        SHORTEST_PATH = True
    else:
        SHORTEST_PATH = False
        
    def is_set(setting):
        return settings.get(setting, None) not in [None, "@NONE"]

    try:

        # RETRIEVE
        if app.server.debug: print(session_id, "> update_graph > retrieve data")
        graph = get_graph(session_id)
        df_nodes = get_dataframe(session_id, "nodes")
        df_edges = get_dataframe(session_id, "edges")
        path_ids = []

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
            if not dataframe_exists(session_id, "nodes"): raise PreventUpdate("Dataframe seems empty..")
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
            network=no_update, selection=no_update,
            loading=html.Div() 
        )
        if app.server.debug: print(session_id, "> update_graph > graph is not empty")
                
        # DERIVATED DATAFRAMES
        if is_set("COL_NODES_LABEL"): 
            if app.server.debug: print(session_id, "> update_graph > obtain labels")
            df_nodes_label = df_nodes[COL_NODES_LABEL]

        if is_set("COL_NODES_SIZE"): 
            if app.server.debug: print(session_id, "> update_graph > obtain nodes sizes")
            df_nodes_size = df_nodes[COL_NODES_SIZE]

        if is_set("COL_EDGES_FROM") and is_set("COL_EDGES_TO"):
            df_edges_group = df_edges[[COL_EDGES_FROM, COL_EDGES_TO]].astype("string").groupby([COL_EDGES_FROM, COL_EDGES_TO])

        if is_set("COL_EDGES_WEIGHT"):
            if app.server.debug: print(session_id, "> update_graph > obtain edges weights")
            df_edges_weight = df_edges[COL_EDGES_WEIGHT]

        if is_set("COL_FOCUS_ON"):
            df_focus = df_nodes[COL_FOCUS_ON]

        def get_label(id):
            if settings.get("SHOW_NODES_LABELS", True) == False: return None
            if is_set("COL_NODES_LABEL"): return get_value_matching_index(df_nodes_label, id)
            return str(id)

        def get_edge_size(id, u, v):
            if is_set("COL_EDGES_WEIGHT"): return get_value_matching_index(df_edges_weight, id, 1)
            
            if is_set("COL_EDGES_FROM") and is_set("COL_EDGES_TO"): 
                try: 
                    return df_edges_group.get_group((str(u), str(v))).count()[0]
                except:
                    return 1

        # SET GRAPH ATTRIBUTES
        if app.server.debug: print(session_id, "> update_graph > nx_nodes")

        ## Create nx_nodes
        nx_nodes = {
            id: {
                "value":  get_value_matching_index(df_nodes_size, id, 0) if is_set("COL_NODES_SIZE") else 0,
                "focus":  str(get_value_matching_index(df_focus, id)) if is_set("COL_FOCUS_ON") else None,
                **({"group": "@NOT_FOCUS"},{})[is_set("COL_FOCUS_ON")],
                "label": get_label(id),
            } for id in graph.nodes()
        }

        ## Keep only focus group
        if is_set("COL_FOCUS_ON") and is_set("COL_FOCUS_VALUE"):
            if app.server.debug: print(session_id, "> update_graph > nx_nodes > keep focus")
            focus_nodes_id = [id for id,options in nx_nodes.items() if options.get("focus") == COL_FOCUS_VALUE]
            focus_nodes_neigh = {neigh_id for node_id in focus_nodes_id for neigh_id in graph.neighbors(node_id)}
            if settings.get("FOCUS_NEIGHBORS_NEIGHBORS", False): 
                focus_nodes_neigh = focus_nodes_neigh.union({neigh_neigh_id for neigh_id in focus_nodes_neigh for neigh_neigh_id in graph.neighbors(neigh_id)})

            focus_nodes_to_keep = set(focus_nodes_id).union(focus_nodes_neigh)
            graph.remove_nodes_from([id for id in graph.nodes() if id not in focus_nodes_to_keep])
            nx_nodes = {id: {"group" : ("@NOT_FOCUS", COL_FOCUS_VALUE)[options.get("focus") == COL_FOCUS_VALUE], **options} for id,options in nx_nodes.items() if id in focus_nodes_to_keep}

        ## Change group to @PATH if shortest-path
        if SHORTEST_PATH:
            select_nodes = selection.get("nodes", [])
            node_id_1, node_id_2 = select_nodes[0], select_nodes[1]
            try:
                path_ids = nx.shortest_path(graph, source=node_id_1, target=node_id_2)
                for id, options in nx_nodes.items():
                    if id in path_ids: options["group"] = "@PATH"
            except Exception:
                pass            

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
                # "title": e_options.get("id", "") if is_set("COL_EDGES_ID") else f"{u}-{v}",
                "value": get_edge_size(e_options["id"], u, v),
                # "label": e_options.get("id", "") if is_set("COL_EDGES_ID") else "",
                "dashes": (u in path_ids and v in path_ids and u != v),
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
            network={"data": net_data, "options": net_options},
            loading=html.Div(),
            selection={"nodes": path_ids, "edges": []}
        )

    except Exception as e: 
        print(e)
        return dict(
            alert=True, alert_message=graph_alert_message(str(e.args[0])),
            network=no_update,
            loading=html.Div(), selection=no_update
        )    


# SHOW SELECTION 
@app.callback(
    dict(
        title=Output("card_selected_node_header", "children"),
        body=Output("card_selected_node_body", "children"),
    ),
    State(store_id, "data"),
    Input("network", "selection"),
    # Input("show_selected_node_switch", "value"),
)
def get_selected_nodes(session_id, selection):
    if not graph_exists(session_id): raise PreventUpdate("Dataframe seems empty..")
    if not selection: raise PreventUpdate
    if len(selection.get("nodes", [])) < 1: raise PreventUpdate()

    nodes = selection.get("nodes", [])
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
        "Betweenness centrality": round(graph_betweenness_centrality.get(node_id),2),
        "Clustering coeff": round(node_clustering_coeff,2),
    }

    body =  [html.P(f"{k}: {v}") for k,v in infos.items()] + \
            [html.Hr()] + \
            [html.P(f"{k}: {v}")for k,v in metrics.items()]
    return dict(title=title, body=body)
