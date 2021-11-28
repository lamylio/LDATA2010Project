# %% Import the application and callbacks
from app import app, store_data, store_graph

# %% Setup the layouts
from dash.html import Div
from dash_bootstrap_components import Container
from dash.dcc import Store
from layouts import layout

app.layout = Container(
    [
        Store(id=store_data, storage_type='local'),
        Store(id=store_graph, storage_type='local'), 
        layout
        # Div(id="page-content", className="h-100") # fn:render_page_content()
    ],
    fluid=True,
    class_name="h-100 w-100 p-0 m-0 g-0",
    style={"overflow": "hidden"}
)

# %% Run the server
# In order to start the server, go to "Debugger" and/or click "Run"
# Or type "python3 main.py" in the console
# View the result : https://replit.llamy.be

app.run_server(port=80, debug=True)
