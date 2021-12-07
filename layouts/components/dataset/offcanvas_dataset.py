from layouts.requirements import dbc, html, dcc
from layouts.components.dataset.import_zone import layout as import_zone
from dash.dcc import Store

layout = dbc.Offcanvas(

    [
        html.H4(id="data_name", className="text-break"),
        html.Br(),
        import_zone,

        html.Br(),
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
        dbc.Button("Load", id="import_dataset", class_name="d-block mx-auto text-center", size="md"),
        html.Br(),
        html.Div([
            html.H4("Columns to remove"),
            dcc.Dropdown(id="columns", multi=True, options=[]),
            html.Br(),
            dbc.Button("Validate", id="validate_dataset", class_name="d-block mx-auto text-center", size="md")
        ], id="div_columns", style={"display": "none"}),
        Store(data=False, id="is_data_loaded"),
        Store(data=False, id="are_columns_picked")
    ],
        
    id="offcanvas-dataset",
    title="Data importation",
    is_open=False,
    placement="end"
)
