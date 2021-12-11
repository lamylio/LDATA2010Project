from app import *
from requirements import *
from storage import *

@app.callback(
    Output(store_settings, "data"),

    State(store_id, "data"),
    Input(store_settings, "data"),

    Input("select_column_nodes_id", "value"),
    Input("select_column_nodes_label", "value"),
    Input("select_column_nodes_size", "value"),

    Input("show_nodes_label_switch", "value"),

    Input("select_column_edges_from", "value"),
    Input("select_column_edges_to", "value"),
)
def update_settings(
    session_id, settings, 
    column_nodes_id, column_nodes_label, column_nodes_size,
    show_nodes_label,
    column_edges_from, column_edges_to,
):
    if not graph_exists(session_id) and not settings_exists(session_id) : return {}
    if app.server.debug: print(session_id, "> update_settings")
    params = settings or {}
    params.update({
        "COL_NODES_ID": column_nodes_id,
        "COL_NODES_LABEL": column_nodes_label,
        "COL_NODES_SIZE": column_nodes_size,

        "SHOW_NODES_LABELS": bool(show_nodes_label),

        "COL_EDGES_FROM": column_edges_from,
        "COL_EDGES_TO": column_edges_to,
    })
    return params


@app.callback(
    Output(store_columns, "data"),
    State(store_id, "data"),
    Input("all_loaded", "data")
)
def update_columns_local(session_id, _):
    if not dataframe_exists(session_id, "nodes") and not dataframe_exists(session_id, "edges") : raise PreventUpdate
    if app.server.debug: print(session_id, "> update_columns_local")
    return {"nodes": get_dataframe(session_id, "nodes").columns, "edges": get_dataframe(session_id, "edges").columns}


@app.callback(
    Output("accordion_columns", "active_item"),
    Input("all_loaded", "data")
)
def open_accordion_once_data_loaded(all_loaded):
    if not all_loaded: raise PreventUpdate
    return "accordion_nodes"

@app.callback(
    Output("select_column_nodes_id", "options"),
    Output("select_column_nodes_label", "options"),
    Output("select_column_nodes_size", "options"),

    Output("select_column_edges_to", "options"),
    Output("select_column_edges_from", "options"),

    Output("select_column_nodes_id", "placeholder"),
    Output("select_column_nodes_label", "placeholder"),
    Output("select_column_nodes_size", "placeholder"),

    Output("select_column_edges_to", "placeholder"),
    Output("select_column_edges_from", "placeholder"),
    State(store_id, "data"),
    Input("all_loaded", "data"),
)
def update_selects_columns_inputs(session_id, _):

    if not dataframe_exists(session_id, "nodes") and not dataframe_exists(session_id, "edges") : raise PreventUpdate
    else: columns = {"nodes": get_dataframe(session_id, "nodes"), "edges": get_dataframe(session_id, "edges")}

    placeholder = ["Please select"] * 5

    nodes = [{"label": col, "value": col} for col in columns.get("nodes").columns]
    edges =  [{"label": col, "value": col} for col in columns.get("edges").columns]

    nodes_int = [{"label": col, "value": col} for col in columns.get("nodes").select_dtypes("int").columns]
    nodes_neib = [{"label": "[BY NEIGHBORS]", "value": "@NEIGHBORS"}] + nodes_int
    return (
        nodes,
        nodes,
        nodes_neib,
        edges,
        edges,
        *placeholder)