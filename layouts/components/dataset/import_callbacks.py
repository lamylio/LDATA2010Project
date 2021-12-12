from app import *
from storage import *
from requirements import *

from utils import parse_file_contents

up_default = html.Div([
 html.A('Drag and Drop or Select file', style={"cursor": "pointer"}, className="font-bold")
])

def load_and_save(session_id, type, content, filename, separator, nas):
    nas_val = nas.split(",")
    if content is None : return False
    try :
        df = parse_file_contents(content, filename, separator, nas_val) 
        if not isinstance(df, DataFrame): raise Exception
    except: return False
    if not df.empty: save_dataframe(session_id, df, type, filename)
    ex = dataframe_exists(session_id, type)
    if app.server.debug: print("load_and_save >", type, ">", session_id, ">", ex)
    return ex


@app.callback(Output("offcanvas_dataset", "is_open"), Input("btn-dataset", "n_clicks"), Input("all_loaded", "data"), State("offcanvas_dataset", "is_open"))
def toggle_offcanvas_dataset(click, all_loaded, is_open):
    if all_loaded and is_open: return False
    return click is not None


# ==========================================

# Show name of data uploaded
@app.callback(
    Output("data_nodes_name", "children"), Output("data_edges_name", "children"), 
    Output("upload_nodes", "children"), Output("upload_edges", "children"),
    Input(store_id, "data"), Input("upload_nodes", "filename"), Input("upload_edges", "filename"), Input("offcanvas_dataset", "is_open"), 
)
def show_selected_or_loaded_filenames(session_id, name_nodes, name_edges, _):
    nn = name_nodes or get_dataframe_name(session_id, "nodes") or "Please select nodes file."
    ne = name_edges or  get_dataframe_name(session_id, "edges") or "Please select edges file."
    un = name_nodes or up_default
    ue = name_edges or up_default
        
    return [nn, ne, un, ue]

# ==========================================

@app.callback(
    Output("nodes_loaded", "data"),
    Output("edges_loaded", "data"),
    Output("loading_datasets", "children"),

    Input("validate_datasets", "n_clicks_timestamp"),

    State('upload_nodes', 'contents'), State('upload_nodes', 'filename'), 
    State('upload_edges', 'contents'), State('upload_edges', 'filename'),
    State("separator", "value"), State("nas", "value"),
    State(store_id, "data")
)
def import_datasets(_, upload_nodes_contents, upload_nodes_filename, upload_edges_contents, upload_edges_filename, separator, nas, session_id):
    nc = (False, load_and_save(session_id, "nodes", upload_nodes_contents, upload_nodes_filename, separator, nas))[upload_nodes_contents != None]
    ec = (False, load_and_save(session_id, "edges", upload_edges_contents, upload_edges_filename, separator, nas))[upload_edges_contents != None]
    return (nc, ec, html.Div())

# ==========================================

@app.callback(
    Output("alert_nodes", "is_open"),
    Output("alert_edges", "is_open"),
    Output("all_loaded", "data"),

    Input("nodes_loaded", "data"),
    Input("edges_loaded", "data"),
    State("validate_datasets", "n_clicks")
)
def nodes_or_edges_is_loaded(nodes_loaded, edges_loaded, clicked):
    if not clicked: raise PreventUpdate
    return (not nodes_loaded, not edges_loaded, nodes_loaded and edges_loaded)

# ==========================================