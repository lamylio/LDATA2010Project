from sys import argv
from uuid import uuid4
from glob import glob
from os import remove

# %% Import the application and callbacks
from app import *
from callbacks import *

# %% Setup the layouts
from requirements import dbc, dbc, Store
from layouts import configurator, tabs
from layouts.components import datasets_import

def serve_layout():
    session_id = str(uuid4())
    return dbc.Container([
        Store(data=session_id, id=store_id, storage_type="local"),

        Store(data={}, id=store_settings, storage_type="memory"), # Maybe local in future
        Store(data={}, id=store_columns, storage_type="memory"), # Maybe local in future
        Store(data={}, id=store_graph, storage_type="memory"),
        dbc.Row([
            dbc.Col(configurator, width=3, xxl=2, style={"height": "100vh"}),
            dbc.Col(tabs, width=9, xxl=10, class_name="p-0", style={"height": "100vh"}),
            datasets_import
        ], class_name="w-100 h-100 g-0")
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
debug = argv[1] if len(argv) > 1 else False
app.run_server(host="0.0.0.0", debug=debug, dev_tools_hot_reload=False, dev_tools_ui=True)