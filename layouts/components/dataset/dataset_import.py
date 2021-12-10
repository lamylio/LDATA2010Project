from requirements import dbc, html, dcc, Store

from layouts.components.dataset.import_callbacks import up_default

layout = dbc.Offcanvas(

    [
        dbc.Alert([], id="alert_nodes", is_open=False, duration=5000, style={"position": "fixed", "top": 10, "left": 10, "zIndex": 9999}, color="danger", class_name="mx-auto text-center h2"),
        dbc.Alert([], id="alert_edges", is_open=False, duration=5000, style={"position": "fixed", "top": 10, "left": 10, "zIndex": 9999}, color="danger", class_name="mx-auto text-center h2"),

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
            html.Br(),
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
        ]),
        # html.Div([
        #     html.H4("Columns to remove"),
        #     dcc.Dropdown(id="columns", multi=True, options=[]),
        #     html.Br(),
        #     
        # ], id="div_columns", style={"display": "none"}),

        html.Center([
            dbc.Button("Validate", id="validate_datasets", class_name="d-block mx-auto text-center", size="md"),
        ]),

        Store(data=False, id="nodes_loaded"),
        Store(data=False, id="edges_loaded"),
        Store(data=False, id="all_loaded"),
    ],
        
    id="offcanvas_dataset",
    title="Data importation",
    is_open=False,
    placement="start"
)