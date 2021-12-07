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
alert = "alert"

dataset_name = "@DATASET_NAME"

# %% Data storage

storage = {}

def get_dataframe(session_id):
    from pandas import DataFrame
    d = storage.get(session_id, {}).copy()
    del d[dataset_name]
    return DataFrame.from_dict(d)

def save_dataframe(session_id, dataframe, df_name=None):    
    if session_id in storage and not df_name: df_name = storage[session_id][dataset_name]
    storage[session_id] = dataframe.to_dict(orient="list")
    storage[session_id][dataset_name] = df_name