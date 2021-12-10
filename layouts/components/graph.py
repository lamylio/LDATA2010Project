from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from dash import callback_context
from requirements import html, dbc

# from visdcc import Network
from pyvis.network import Network

layout = html.Div(
    [
        dbc.Card([
            dbc.CardHeader(html.H3("No data available")),
            dbc.CardBody([
                "There is no data available to display.", 
                html.Br(),
                "Please click on the data importation button first."])
        ], id="net_card", outline=True, style={}, class_name="w-50 mx-auto mt-5"),

        html.Iframe(id="network", className="w-100", style={"height": "100%", "width": "100%", "position": "absolute", "top": "-25px", "right": "-25px"}),
    ],
    id="net",
    className="h-100"
)


# @app.callback(
#     Output("graph", "data"),
#     Output(store_graph, "data"),
#     Input("edges_graph", "data"),
#     Input("nodes_graph", "data"),
#     Input(store_graph, "data")
# )
# def update_graph(edges_graph, nodes_graph, store_graph):
#     ctx = callback_context
#     print("DEBUG: graph update")
#     graph_data = store_graph or {"edges": [], "nodes": []}
#     if ctx.triggered:
#         input = ctx.triggered[0]['prop_id'].split('.')[0]
#         if input == "edges_graph": graph_data["edges"] = edges_graph
#         elif input == "nodes_graph": graph_data["nodes"] = nodes_graph

#     return (graph_data, graph_data)