import dash_bootstrap_components as dbc
from dash import dcc
from dash.html import Div

layout = Div([
    dcc.Location("url"),
    dbc.NavbarSimple(
        [
            dbc.NavLink("Dataset", href="/import", active="exact"),
            dbc.NavLink("Graphic", href="/graph", active="exact"),
            dbc.NavLink("Table", href="/table", active="exact")
        ],  
        brand="Graph visualization app",
        color="light"
    )
])