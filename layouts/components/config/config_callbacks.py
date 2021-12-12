from app import *
from requirements import *
from storage import *

@app.callback(
    Output(store_settings, "data"),
    inputs=dict(
        session_id=State(store_id, "data"),
        session_settings=Input(store_settings, "data"),
        options=dict(
            COL_NODES_ID=Input("select_column_nodes_id", "value"),
            COL_NODES_LABEL=Input("select_column_nodes_label", "value"),
            COL_NODES_SIZE=Input("select_column_nodes_size", "value"),
            SHOW_NODES_LABELS=Input("show_nodes_label_switch", "value"),
            GLOBAL_NODES_COLOR=Input("input_nodes_color", "value"),
            
            COL_EDGES_FROM=Input("select_column_edges_from", "value"),
            COL_EDGES_TO=Input("select_column_edges_to", "value"),

            GRAPH_LAYOUT=Input("input_layout_selector", "value"),
        )
    )
)
def update_settings(
    session_id, session_settings, options : dict
):
    if not graph_exists(session_id) and not settings_exists(session_id) : return {}
    if app.server.debug: print(session_id, "> update_settings")
    params = session_settings or {}
    params.update(options)
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