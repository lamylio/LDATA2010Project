from app import *
from storage import *
from layouts.requirements import *
from dash import no_update

up_default = html.Div([
 html.A('Drag and Drop or Select file', style={"cursor": "pointer"}, className="font-bold")
])

def parse_contents(contents, filename, separator, nas):
    from pandas import read_csv, read_table
    from base64 import b64decode
    from io import StringIO
    _, content_string = contents.split(',')
    decoded = b64decode(content_string)
    print(separator)
    if 'csv' in filename.lower():
        df = read_csv(StringIO(decoded.decode('utf-8')), sep=separator, na_values=nas)
    elif 'txt' in filename:
        df = read_table(StringIO(decoded.decode('utf-8')), sep=separator, na_values=nas, engine="python")
    else :
        return None

    df.columns = df.columns.str.strip("#").str.upper().str.replace(" ", "_")
    return df


def load_and_save(session_id, type, content, filename, separator, nas):
    nas_val = nas.split(",")
    df = parse_contents(content, filename, separator, nas_val)
    if not df.empty: 
        save_dataframe(session_id, df, type, filename)
        return (no_update, no_update, True)
    else : 
        return ([f"Unable to load {filename}, please check the format and separator."], True, False)

# ==========================================

@app.callback(
    Output("data_nodes_name", "children"), Output("data_edges_name", "children"), 
    Output("upload_nodes", "children"), Output("upload_edges", "children"),
    Input(store_id, "data"), Input("upload_nodes", "filename"), Input("upload_edges", "filename"), Input("offcanvas_dataset", "is_open"), 
)
def show_selected_or_loaded_filenames(session_id, name_nodes, name_edges, is_open):
    if not is_open: raise PreventUpdate

    nn = name_nodes or get_dataframe_name(session_id, "nodes") # or "Please select nodes file."
    ne = name_edges or  get_dataframe_name(session_id, "edges") or "Please select edges file."
    un = name_nodes or up_default
    ue = name_edges or up_default
        
    return [nn, ne, un, ue]

# ==========================================

@app.callback(
    Output("alert_nodes", "children"), Output("alert_nodes", "is_open"), 
    Output("nodes_loaded", "data"), 
    Input(store_id, 'data'),
    # Input('import_nodes', 'n_clicks_timestamp'), 
    
    Input('upload_nodes', 'contents'), State('upload_nodes', 'filename'),  
    State("separator", "value"), State("nas", "value")
)
def load_and_save_nodes(session_id, content, filename, separator, nas):
    if content is None: return (no_update, no_update, dataframe_exists(session_id, "nodes"))
    return load_and_save(session_id, "nodes", content, filename, separator, nas)

@app.callback(
    Output("alert_edges", "children"), Output("alert_edges", "is_open"), 
    Output("edges_loaded", "data"), 
    Input(store_id, 'data'),
    
    Input('upload_edges', 'contents'), State('upload_edges', 'filename'),  
    State("separator", "value"), State("nas", "value")
)
def load_and_save_edges(session_id, content, filename, separator, nas):
    if content is None: return (no_update, no_update, dataframe_exists(session_id, "edges"))
    return load_and_save(session_id, "edges", content, filename, separator, nas)

# ==========================================

@app.callback(
    Output("input_column_nodes_id", "style"), Output("input_column_nodes_label", "style"), Output("input_column_edges", "style"),
    Input("nodes_loaded", "data"),Input("edges_loaded", "data")
)
def show_column_selection(nodes_loaded, edges_loaded):
    nid = (no_update, {})[nodes_loaded]
    eid = (no_update, {})[edges_loaded]
    return (nid, nid, eid)


@app.callback(
    Output("column_nodes_id", "options"),
    Output("column_nodes_label", "options"),
    Input(store_id, "data"),
    Input("nodes_loaded", "data")
)
def add_options_nodes_selection(session_id, nodes_loaded):
    if not nodes_loaded: raise PreventUpdate
    df = get_dataframe(session_id, "nodes")
    res = [{"label": col, "value": col} for col in list(df.columns)]
    return (res, res)

@app.callback(
    Output("column_edges_to", "options"),
    Output("column_edges_from", "options"),
    Input(store_id, "data"),
    Input("edges_loaded", "data")
)
def add_options_edges_selection(session_id, edges_loaded):
    if not edges_loaded: raise PreventUpdate
    df = get_dataframe(session_id, "edges")
    res = [{"label": col, "value": col} for col in list(df.columns)]
    return (res, res)


# ==============================================

@app.callback(
    Output("nodes_graph", "data"),
    Input("column_nodes_id", "value"),
    Input("column_nodes_label", "value"),
    State(store_id, "data")
)
def create_nodes(column_nodes_id, column_nodes_label, session_id):
    if not column_nodes_id or not column_nodes_label: raise PreventUpdate
    df = get_dataframe(session_id, "nodes")
    nodes = [{"id": id, "label": str(label)} for _, id, label in df[[column_nodes_id, column_nodes_label]].itertuples()]
    return nodes

@app.callback(
    Output("edges_graph", "data"),
    Input("column_edges_from", "value"),
    Input("column_edges_to", "value"),
    State(store_id, "data")
)
def create_edges(column_edges_from, column_edges_to,  session_id):
    if not column_edges_from or not column_edges_to: raise PreventUpdate
    df = get_dataframe(session_id, "edges")
    edges = [{"id": f"{n_from}-{n_to}", "from": n_from, "to": n_to} for _, n_from, n_to in df[[column_edges_from, column_edges_to]].itertuples()]
    return edges


