from app import app, store_id
from storage import dataframe_exists
from requirements import *
from visdcc import Network

@app.callback(
    dict(
        tabs=Output("tabs", "class_name"),
        no_data=Output("card_no_data", "className")
    ),
    State(store_id, "data"),
    Input("all_loaded", "data"),
)
def show_tabs(session_id, _):
    if dataframe_exists(session_id, "nodes") and dataframe_exists(session_id, "edges"): return dict(tabs="", no_data="d-none")
    return dict(tabs="d-none", no_data="")


@app.callback(
    Output("tab_network", "children"),
    State("tabs", "active_tab"),
    Input("store_network", "data"),
    State("tabs", "class_name")
)
def draw_network_tab(active_tab, store_network, tabs_class):
    if not store_network: raise PreventUpdate()
    if active_tab != "network": raise PreventUpdate()
    if tabs_class == "d-none": raise PreventUpdate()
    data = store_network.get("data")
    options = store_network.get("options")

    return Network(id="network", options=options, data=data, style={"height": "96vh", "width": "100%"})
