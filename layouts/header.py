import dash_bootstrap_components as dbc
from dash import dcc, html

layout = html.Div(
    [
        dcc.Location("url"),
        dbc.Navbar(
            dbc.Nav(
                [
                    dbc.NavLink("Dataset", className="h4", href="/import", active="partial"),

                    dbc.NavLink("Graphic", className="h4", href="/graph", active="partial"),

                    dbc.NavLink("Table", className="h4", href="/table", active="partial")
                
                ],
                justified="center",
                horizontal="center",
                navbar=True,
                class_name="d-flex justify-content-around w-100"
            ),
        style={"border-bottom": "5px solid var(--dark)"}
        )
    ]
)