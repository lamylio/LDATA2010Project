# %% Application imports
from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc

import layouts # ours

# %% Data manipulation imports
import pandas as pd
import numpy as np

# %% TEMP data setup
data = pd.DataFrame()

# %% Create the app
app = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])

# %% Define the layout

app.layout = html.Div(
    [
        layouts.header,
        dbc.Container(id="page-content") # fn:render_page_content()
    ]
)

# %% Navigation callback to render appropriate page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    path = pathname[1:]

    if path in ["", "/", "home", "graph"]:
        if data is None: return layouts.importation
        return layouts.graph

    elif path in ["import", "importation"]:
        return layouts.importation

    elif path in ["table", "data"]:
        return layouts.table

    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {path} was not recognised..."),
        ]
    )
# %%
app.run_server(debug=True)