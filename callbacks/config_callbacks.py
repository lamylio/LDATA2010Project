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
            
            NODES_COLOR=Input("input_nodes_color", "value"),
            NODES_OPACITY=Input("input_nodes_opacity", "value"),
            
            COL_EDGES_ID=Input("select_column_edges_id", "value"),
            COL_EDGES_FROM=Input("select_column_edges_from", "value"),
            COL_EDGES_TO=Input("select_column_edges_to", "value"),
            COL_EDGES_WEIGHT=Input("select_column_edges_weight", "value"),
            EDGES_COLOR_INHERIT=Input("select_edges_color", "value"),
            EDGES_COLOR=Input("input_edges_color", "value"),
            EDGES_OPACITY=Input("input_edges_opacity", "value"),
            EDGES_ARROWS=Input("input_edges_arrows", "value"),

            COL_FOCUS_ON=Input("select_column_focus_on", "value"),
            COL_FOCUS_VALUE=Input("select_column_focus_value", "value"),

            FIXED_X_Y=Input("input_fixed_x_y", "value"),
            GRAPH_LAYOUT=Input("input_layout_selector", "value"),
        )
    )
)
def update_settings(
    session_id, session_settings, options : dict
):
    if app.server.debug: print(session_id, "> update_settings")
    params = session_settings or {}
    params.update(options)
    print(params)
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

    Output("select_column_edges_id", "options"),
    Output("select_column_edges_to", "options"),
    Output("select_column_edges_from", "options"),
    Output("select_column_edges_weight", "options"),

    Output("select_column_focus_on", "options"),
    # --

    Output("select_column_nodes_id", "placeholder"),
    Output("select_column_nodes_label", "placeholder"),
    Output("select_column_nodes_size", "placeholder"),

    Output("select_column_edges_id", "placeholder"),
    Output("select_column_edges_to", "placeholder"),
    Output("select_column_edges_from", "placeholder"),
    Output("select_column_edges_weight", "placeholder"),    

    Output("select_column_focus_on", "placeholder"),

    State(store_id, "data"),
    Input("all_loaded", "data"),
)
def update_selects_columns_inputs(session_id, _):

    if not dataframe_exists(session_id, "nodes") and not dataframe_exists(session_id, "edges") : raise PreventUpdate
    else: columns = {"nodes": get_dataframe(session_id, "nodes"), "edges": get_dataframe(session_id, "edges")}

    placeholder = ["Please select"] * 8

    nodes = [{"label": col, "value": col} for col in columns.get("nodes").columns]
    edges =  [{"label": col, "value": col} for col in columns.get("edges").columns]

    nodes_num_cols = list(columns.get("nodes").select_dtypes("int").columns) + list(columns.get("nodes").select_dtypes("float").columns)
    nodes_str_cols = list(columns.get("nodes").select_dtypes("object").columns)
    edges_num_cols = list(columns.get("edges").select_dtypes("int").columns) + list(columns.get("edges").select_dtypes("float").columns)

    nodes_num = [{"label": col, "value": col} for col in nodes_num_cols] + [{"label": "[NONE]", "value": "@NONE"}]
    nodes_str = [{"label": col, "value": col} for col in nodes_str_cols] + [{"label": "[ID]", "value": "@NONE"}]
    edges_num = [{"label": col, "value": col} for col in edges_num_cols] + [{"label": "[NONE]", "value": "@NONE"}]
    return (
        nodes,
        nodes_str,
        nodes_num,

        edges,
        edges,
        edges,
        edges_num,
        nodes,

        *placeholder)
    
    
    
@app.callback(
    Output("card_selected", "className"),
    State(store_id, "data"),
    Input("show_selected_node_switch", "value"),
)
def show_card_of_selected_node(session_id, show_selected):
    if not show_selected: return "invisible"
    if graph_exists(session_id): return "visible"
    return "invisible"


@app.callback(
    Output("select_column_focus_value", "options"),
    Output("select_column_focus_value", "placeholder"),

    State(store_id, "data"),
    Input("select_column_focus_on", "value"),

)
def update_focus_select_value(session_id, focus_on):
    if not focus_on: raise PreventUpdate
    if not dataframe_exists(session_id, "nodes") : raise PreventUpdate

    df = get_dataframe(session_id, "nodes")
    col_by_focus = set(df[focus_on])
    options_by_focus = [{"label": col, "value": col} for col in col_by_focus]

    return (options_by_focus, "Please select")