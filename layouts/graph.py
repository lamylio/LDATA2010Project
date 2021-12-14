from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

from dash import callback_context
from requirements import html, dbc

from visdcc import Network

layout = html.Div(
    [   
        html.Div(id="card_no_data", className="d-none", children=[
            dbc.Card([
                dbc.CardHeader(html.H3("No data available")),
                dbc.CardBody([
                    "There is no data available to display.", 
                    html.Br(),
                    "Please click on the data importation button first."])
            ], id="net_card", outline=True, class_name="w-50 mx-auto mt-5"),
        ]),

        html.Div(id="card_selected", className="invisible", children=[
            dbc.Card(class_name="position-absolute mx-3 mt-5", style={"right": "0px"},children=[
                dbc.CardHeader(id="card_selected_node_header"),
                dbc.CardBody(id="card_selected_node_body")
            ])
        ]),
        Network(id="network", options={"height": "100%", "width": "100%"}, data={"nodes": [], "edges": []}, style={"height": "100%", "width": "100%"})
    ],
    id="net",
    className="h-100"
)