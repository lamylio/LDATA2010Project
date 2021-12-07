from app import app

from dash.dependencies import Input, Output
from layouts.requirements import html, dbc
from layouts import components


layout = html.Div([
    components.graph,

    dbc.Button("Dataset", id="btn-dataset", color="dark", class_name="col-2 mx-auto position-absolute rounded-0", style={"top": "5vh", "right": "5vw", "opacity": 0.8}, size="lg"),
    
    components.offcanvas_dataset
])


@app.callback(Output("offcanvas_dataset", "is_open"), Input("btn-dataset", "n_clicks"))
def toggle_offcanvas_dataset(click):
    return click is not None