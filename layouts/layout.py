from app import app

from dash.dependencies import Input, Output
from layouts.requirements import html, dbc
from layouts import components


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