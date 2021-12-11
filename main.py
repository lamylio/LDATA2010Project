from uuid import uuid4
from glob import glob
from os import remove

# %% Import the application and callbacks
from app import *
from callbacks import *

# %% Setup the layouts
from dash_bootstrap_components import Container
from dash.dcc import Store, Loading
from layouts import layout

def serve_layout():
    session_id = str(uuid4())
    return Container(
    [
        Store(data=session_id, id=store_id, storage_type="local"),

        Store(data={}, id=store_settings, storage_type="session"),
        Store(data={}, id=store_columns, storage_type="session"),
        Store(id=store_graph), 
        layout
    ],
    fluid=True,
    class_name="h-100 w-100 p-0 m-0 g-0",
    style={"overflow": "hidden"}
)

# %% Run the server
# In order to start the server, go to "Debugger" and/or click "Run"
# Or type "python3 main.py" in the console
# View the result : https://replit.llamy.be

cached = glob("cache/*")
networks = glob("networks/*.html")
for f in cached: remove(f)
for f in networks: remove(f)

app.layout = serve_layout
app.title = "LDATA2010 - Graph visualisation"
app.run_server(host="0.0.0.0", debug=False, dev_tools_hot_reload=False)
