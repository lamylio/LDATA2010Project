from uuid import uuid4
# %% Import the application and callbacks
from app import app, store_id, store_graph, alert

# %% Setup the layouts
from dash_bootstrap_components import Container, Alert
from dash.dcc import Store
from layouts import layout

def serve_layout():
    session_id = str(uuid4())
    return Container(
    [
        Store(data=session_id, id=store_id, storage_type="local"),
        Store(id=store_graph, storage_type='local'), 
        Alert([], id=alert, is_open=False, duration=5000, style={"position": "fixed", "top": 10, "right": 10, "zIndex": 9999}, color="danger", class_name="mx-auto text-center h2"),
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
app.run_server(port=80, debug=False)
