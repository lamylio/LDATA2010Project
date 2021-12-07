from layouts.requirements import dbc, html, dcc
from dash.dcc import Store

from layouts.components.dataset.import_callbacks import *



layout = dbc.Offcanvas(

    [
        dbc.Alert([], id="alert_nodes", is_open=False, duration=5000, style={"position": "fixed", "top": 10, "right": 10, "zIndex": 9999}, color="danger", class_name="mx-auto text-center h2"),
        dbc.Alert([], id="alert_edges", is_open=False, duration=5000, style={"position": "fixed", "top": 10, "right": 10, "zIndex": 9999}, color="danger", class_name="mx-auto text-center h2"),

        html.Center([
            dbc.InputGroup([
                dbc.InputGroupText("Separator"),
                dbc.Select(id="separator", options=[
                    {"label": "Tab", "value": "\t"},
                    {"label": "Space", "value": " "},
                    {"label": "Comma", "value": ","},
                    {"label": "Semicolon", "value": ";"}
                ], value="\t")
            ]),
            html.Br(),
            dbc.InputGroup([
                dbc.InputGroupText("NA values"),
                dbc.Input(id="nas", type="text", value="-, -|-, -|-|-, -|-|-|-, -|-|-|-|-")
            ]),

        ]),

        html.Hr(),

        html.Center([
            html.H4("Please select nodes file.", id="data_nodes_name", className="text-break"),
            html.Br(),
            dcc.Upload(
                id='upload_nodes',
                children=up_default,
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center'
                },
                multiple=False
            ),
            html.Br(),
            dbc.InputGroup([
                dbc.InputGroupText("Nodes ID"),
                dbc.Select(id="column_nodes_id"),
            ], id="input_column_nodes_id", style={"display": "none"}),
            dbc.InputGroup([
                dbc.InputGroupText("Nodes Label"),
                dbc.Select(id="column_nodes_label")
            ], id="input_column_nodes_label", style={"display": "none"}),
            html.Br(),
            dbc.Button("Load nodes", id="import_nodes", class_name="mx-auto text-center", size="md", style={"display": "none"}),
        ]),

        html.Hr(),

        html.Center([
            html.H4("Please select edges file.", id="data_edges_name", className="text-break"),
            html.Br(),
            dcc.Upload(
                id='upload_edges',
                children=up_default,
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center'
                },
                multiple=False
            ),
            html.Br(),
            dbc.InputGroup([
                dbc.InputGroupText("EDGES FROM", class_name="w-50 text-center"),
                dbc.InputGroupText("EDGES TO", class_name="w-50 text-center"),
                dbc.Select(id="column_edges_from"),
                dbc.Select(id="column_edges_to")
            ], id="input_column_edges", class_name="w-100", style={"display": "none"}),
            html.Br(),
            dbc.Button("Load edges", id="import_edges", class_name="mx-auto text-center", size="md", style={"display": "none"}),
        ]),

        html.Br(),

        # html.Div([
        #     html.H4("Columns to remove"),
        #     dcc.Dropdown(id="columns", multi=True, options=[]),
        #     html.Br(),
        #     dbc.Button("Validate", id="validate_dataset", class_name="d-block mx-auto text-center", size="md")
        # ], id="div_columns", style={"display": "none"}),

        Store(data=False, id="nodes_loaded"),
        Store(data=False, id="edges_loaded"),
        Store(data=False, id="nodes_graph"),
        Store(data=False, id="edges_graph"),
    ],
        
    id="offcanvas_dataset",
    title="Data importation",
    is_open=False,
    placement="end"
)