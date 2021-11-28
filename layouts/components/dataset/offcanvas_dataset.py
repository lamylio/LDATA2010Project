from layouts.requirements import dbc, html, dcc
from layouts.components.dataset.import_zone import layout as import_zone

layout = dbc.Offcanvas(

    [
        html.H4(id="data_name"),
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
        html.H4("Columns to keep"),
        dcc.Dropdown(id="columns", multi=True, options=[]),
        html.Br(),
        dbc.Button("Validate (not working, yet)", id="validate", class_name="mx-auto text-center", size="md")
    ],
        
    id="offcanvas-dataset",
    title="Data importation",
    is_open=False,
    placement="end"
)
