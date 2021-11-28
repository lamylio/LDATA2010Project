from dash import Dash
from dash_bootstrap_components.themes import LITERA, BOOTSTRAP
from dash.dcc import Store

# %% Create the app
app = Dash(__name__, external_stylesheets=[BOOTSTRAP, LITERA])
server = app.server

# %% Variable storing
store_data = "store_local_data"
store_graph = "store_local_graph"
