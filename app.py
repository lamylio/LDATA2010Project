from dash import Dash
from dash_bootstrap_components.themes import LITERA, BOOTSTRAP
from flask_caching import Cache

# %% Create the app
app = Dash("Graphiz by Lionel", external_stylesheets=[BOOTSTRAP, LITERA], suppress_callback_exceptions=True, title="LDATA2010 - Graph visualisation", )
cache = Cache(app.server, config={
    "CACHE_TYPE": 'filesystem',
    "CACHE_DIR": 'cache',
    "CACHE_THRESHOLD": 100
})
server = app.server

# %% Variable storing
store_id = "session_id"
store_columns = "datasets_columns"
store_settings = "visual_settings"
store_graph = "store_local_graph"

alert = "alert"

# ===
dataframes = {}
options = {}
graphs = {}