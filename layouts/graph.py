from requirements import html, dbc, Store
from visdcc import Network

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

        html.Div(id="card_selected", className="", style={"z-Index": 9999}, children=[
            dbc.Card(class_name="position-absolute mx-3 mt-5", style={"right": "0px"}, children=[
                dbc.CardHeader(id="card_selected_node_header", class_name="bold"),
                dbc.CardBody(id="card_selected_node_body")
            ])
        ]),

        dbc.Tabs(id="tabs", class_name="d-none", children=[
            dbc.Tab(id="tab_network", tab_id="network", label="Classic network", active_label_class_name="bold bg-primary text-light", style={"height": "100%", "width": "100%"}, children=[
                Network(id="network", options={}, data={"nodes": [], "edges": []}, style={"height": "96vh", "width": "100%"})
            ]),
            dbc.Tab(id="tab_matrix", tab_id="matrix", label="Adjacency matrix", active_label_class_name="bold bg-primary text-light", style={"height": "100%", "width": "100%"}, children=[
                html.H3("Adjacency matrix to be displayed here")
            ])
        ]),
        Store(id="store_network", storage_type="local")
    ],
    id="net",
    className="h-100"
)
