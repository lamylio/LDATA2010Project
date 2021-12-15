from requirements import html, dbc
from visdcc import Network
from utils import graph_alert_message

layout = html.Div(
    [   
        html.Div(id="card_no_data", className="", children=[
            dbc.Card([
                dbc.CardHeader(html.H4("No data available"), class_name="mb-0 pb-0"),
                dbc.CardBody([
                    html.P([
                        html.P("There is no data available to display..", className="bold"), 
                        "Please import data by clicking on the \"Import\" button on the left.",
                        html.Br(),
                        "Then, select the ID column in nodes settings to start."
                    ])
                ])
            ], id="net_card", outline=True, class_name="w-50 mx-auto mt-5"),
        ]),

        html.Div(id="card_selected", className="", children=[
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