from app import app

from dash.dependencies import Input, Output
from layouts.requirements import html, dbc
from layouts import components

app.layout = html.Div([
    html.Button('Graph', id='btn-nclicks-1', n_clicks=0),
    html.Button('Dataset', id='btn-nclicks-2', n_clicks=0),
    html.Button('Tables', id='btn-nclicks-3', n_clicks=0),
    html.Div(id='container-button-timestamp')
])


layout = html.Div([
    html.Label('Layouts'),
    dcc.Dropdown(
        id = 'first-dropdown',
        options=[
            {'label': 'Ex1', 'value': ''},
            {'label': 'Ex2', 'value': ''},
            {'label': 'Ex3', 'value': ''}
        ],
        value=['', ''],
        multi=True
    )
])

layout = html.Div([
    html.Label('Spacialization'),
    dcc.Dropdown(
        id = 'second-dropdown',
        options=[
            {'label': 'Ex1', 'value': ''},
            {'label': 'Ex2', 'value': ''},
            {'label': 'Ex3', 'value': ''}
        ],
        value=[''],
        multi=True
    )
])


layout = html.Div([
    html.Label('Attributes'),
    dcc.Dropdown(
        id = 'third-dropdown',
        options=[
            {'label': 'Ex1', 'value': ''},
            {'label': 'Ex2', 'value': ''},
            {'label': 'Ex3', 'value': ''}
        ],
        value=[''],
        multi=True
    )
])


layout = html.Div([
    components.graph,
    dbc.Offcanvas([
        dbc.Button("Data importation", id="btn-dataset", color="dark", class_name="mx-autorounded-0", style={"opacity": 0.8}, size="lg"),

    ],id="configurator", backdrop=False, is_open=True),
    
    components.offcanvas_dataset
])


@app.callback(Output("offcanvas_dataset", "is_open"), Input("btn-dataset", "n_clicks"))
def toggle_offcanvas_dataset(click):
    return click is not None

