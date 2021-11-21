# %% Import the application and callbacks
from app import app
from callbacks import *

# %% Setup the layouts
from layouts import header
from dash.html import Div
from dash_bootstrap_components import Container

app.layout = Container(
    [
        header,
        Div(id="page-content", className="h-100") # fn:render_page_content()
    ],
    fluid=True,
    class_name="h-100 w-100 p-0 m-0 g-0",
)

# %% Run the server
# In order to start the server, go to "Debugger" and/or click "Run"
# Or type "python3 main.py" in the console
# View the result : https://replit.llamy.be
app.run_server(host='0.0.0.0', dev_tools_hot_reload=True, dev_tools_hot_reload_interval=10)
