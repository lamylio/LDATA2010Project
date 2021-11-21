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

# %% Run if asked
if __name__ == "__main__":
    app.enable_dev_tools(True)
    app.run_server(debug=True)