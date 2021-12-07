from dash import Dash
from dash_bootstrap_components.themes import LITERA, BOOTSTRAP
from dash.dcc import Store
from flask.globals import session
from flask_caching import Cache
from pandas._config import config

# %% Create the app
app = Dash(__name__, external_stylesheets=[BOOTSTRAP, LITERA])
cache = Cache(app.server, config={
    "CACHE_TYPE": 'filesystem',
    "CACHE_DIR": 'cache',
    "CACHE_THRESHOLD": 100
})
server = app.server

# %% Variable storing
store_id = "session_id"
store_data = "store_local_dataset"
store_graph = "store_local_graph"
store_settings = "store_local_settings"

alert = "alert"

col_dataset_name = "@DATASET_NAME"