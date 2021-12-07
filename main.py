from uuid import uuid4
# %% Import the application and callbacks
from app import *

# %% Setup the layouts
from dash_bootstrap_components import Container
from dash.dcc import Store
from layouts import layout

def serve_layout():
    session_id = str(uuid4())
    return Container(
    [
        Store(data=session_id, id=store_id, storage_type="local"),
        Store(id=store_settings, storage_type='local'),
        Store(id=store_graph, storage_type='local'), 
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

app.layout = serve_layout
app.run_server(host="0.0.0.0", port=80, debug=False, dev_tools_hot_reload=False)
