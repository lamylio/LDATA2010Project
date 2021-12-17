from requirements import html, dbc
from visdcc import Network
from dash.dash_table import DataTable

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
            dbc.Tab(id="tab_network", tab_id="network", label="Graphic", active_label_class_name="bold bg-primary text-light", style={"height": "100%", "width": "100%"}, children=[
                Network(id="network", options={}, data={"nodes": [], "edges": []}, moveTo={"position": {"x": 0, "y": 0, "scale": 0.8}}, style={"height": "96vh", "width": "100%"})
            ]),

            dbc.Tab([
                dbc.Spinner(html.Div(), id="loading_adjacency", color="primary", size="lm", show_initially=False), 
            ], id="tab_matrix", tab_id="matrix", label="Adjacency matrix", active_label_class_name="bold bg-primary text-light", style={"height": "100%", "width": "100%"}),

            dbc.Tab(id="tab_histogram", tab_id="histogram", label="Histograms", active_label_class_name="bold bg-primary text-light", style={"height": "100%", "width": "100%"}, children=[
                dbc.Alert(html.H3("Various histograms to be displayed here: degree, clustering coeff, ... (TODO)", className="p-0 m-0"), class_name="w-100", color="primary"),
                dbc.Row(class_name="placeholder-glow my-3", children=[
                    dbc.Col(style={"min-height": "300px"}, children=[
                        dbc.Card(class_name="w-100 h-100 placeholder col-12")
                    ], id="hist_1"),
                    dbc.Col([
                        dbc.Card(class_name="w-100 h-100 placeholder col-12")
                    ], id="hist_2"),
                ]),
                dbc.Row(class_name="placeholder-glow my-3", children=[
                    dbc.Col(style={"min-height": "300px"}, children=[
                        dbc.Card(class_name="w-100 h-100 placeholder col-12")
                    ], id="hist_3"),
                    dbc.Col([
                        dbc.Card(class_name="w-100 h-100 placeholder col-12")
                    ], id="hist_4"),
                ]),
            ]),

            dbc.Tab(id="tab_nodes", tab_id="dataframe_nodes", label="Dataframe nodes", active_label_class_name="bold bg-primary text-light", style={"height": "90vh", "width": "100%", "overflow": "auto"}, children=[
                DataTable(id="df_nodes", page_size=25, fixed_rows={'headers': True},  style_as_list_view=True, editable=True)
            ]),

            dbc.Tab(id="tab_edges", tab_id="dataframe_edges", label="Dataframe nodes", active_label_class_name="bold bg-primary text-light", style={"height": "90vh", "width": "100%"}, children=[
                DataTable(id="df_edges", page_size=25, fixed_rows={'headers': True},  style_as_list_view=True, editable=True)
            ])

        ]),
    ],
    id="net",
    className="h-100"
)
