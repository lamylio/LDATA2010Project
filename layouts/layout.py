from app import app

from requirements import *
from layouts import components

layout = dbc.Row([
    dbc.Col(components.configurator, width=3, xxl=2, style={"height": "100vh"}),
    dbc.Col(components.graph, width=9, xxl=10, class_name="p-0", style={"height": "100vh"}),
    components.datasets_import
], class_name="w-100 h-100 g-0")

