from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from app import app, store_graph

from dash import callback_context
from layouts.requirements import html

import visdcc

graph_options = {
    "height": "1500px",
    "width": "100%",
    "configure" : {"enabled": False},
    "nodes": {"color": "black"},
    "edges": {},
    "layout": {"improvedLayout": False},
}

layout = html.Div(
    [    
        visdcc.Network(id="graph", options=graph_options, data={"nodes": [], "edges": {}})
    ],
    className="h-100 position-absolute"
)


@app.callback(
    Output("graph", "data"),
    Output(store_graph, "data"),
    Input("edges_graph", "data"),
    Input("nodes_graph", "data"),
    Input(store_graph, "data")
)
def update_graph(edges_graph, nodes_graph, store_graph):
    ctx = callback_context
    print("DEBUG: graph update")
    if not ctx.triggered: return (store_graph, store_graph)
    else: 
        graph_data = store_graph or {}
        input = ctx.triggered[0]['prop_id'].split('.')[0]
        if input == "edges_graph": graph_data["edges"] = edges_graph
        elif input == "nodes_graph": graph_data["nodes"] = nodes_graph

        return (graph_data, graph_data)