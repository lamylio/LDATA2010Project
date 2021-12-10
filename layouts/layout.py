from app import app

from requirements import *
from layouts import components

layout = dbc.Row([
    dbc.Col(components.configurator, width=3, xxl=2),
    dbc.Col(components.graph, width=9, xxl=10, class_name="p-0"),
    components.datasets_import
], class_name="w-100 h-100 g-0")


@app.callback(Output("offcanvas_dataset", "is_open"), Input("btn-dataset", "n_clicks"), Input("all_loaded", "data"), State("offcanvas_dataset", "is_open"))
def toggle_offcanvas_dataset(click, all_loaded, is_open):
    if all_loaded and is_open: return False
    return click is not None

