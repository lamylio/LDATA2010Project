from networkx.algorithms import assortativity
from networkx.algorithms.cluster import triangles
from app import *
from storage import *
from requirements import *

import networkx as nx

@app.callback(
    dict(
        assortativity=Output("graph_assortativity", "children"),
        connectivity=Output("graph_connectivity", "children"),
        transitivity=Output("graph_transitivity", "children"),
        # generalized_degree=Output("graph_generalized_degree", "children"),
        avg_clustering=Output("graph_avg_clustering", "children"),
    ),
    State(store_id, "data"),
    Input("network", "data")
)
def update_various_global_metrics(session_id, _):
    if not graph_exists(session_id): raise PreventUpdate() 
    graph = get_graph(session_id)
    if len(graph.edges) < 1: raise PreventUpdate()
    if app.server.debug: print(session_id, "> update_various_global_metrics")
    return dict(
        assortativity=str(round(nx.degree_assortativity_coefficient(graph), 3)),
        connectivity=str(round(nx.average_node_connectivity(graph), 2)),
        transitivity=str(round(nx.transitivity(graph), 2)),
        avg_clustering=str(round(nx.average_clustering(graph), 2))
    )
