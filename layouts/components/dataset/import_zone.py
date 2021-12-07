
import base64
import io

import pandas as pd
from app import app, store_data, alert, dataset_name, storage, store_id, get_dataframe, save_dataframe
from layouts.requirements import dcc, html, dbc, Input, Output, State, PreventUpdate
from dash import no_update

up_default = html.Div([
    'Drag and Drop or ', html.A('Select Files', style={"cursor": "pointer"}, className="font-bold")
])

layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=up_default,
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center'
        },
        multiple=False
    ),
])

# 1)
# Show the name of the dataset selected
@app.callback(Output("data_name", "children"), Output("upload-data", "children"), Input("upload-data", "filename"), Input("offcanvas-dataset", "is_open"), Input(store_id, "data"))
def show_selected_filename(filename, is_open, session_id):
    if not is_open: raise PreventUpdate
    if filename: return [filename, f"File selected!"]
    
    data = storage.get(session_id, {})
    return [data.get(dataset_name, "Data not yet imported."), up_default]

# 2)
# Retrieve the data from the upload button, and save it in json to the storage
@app.callback(
    Output(alert, "children"), Output(alert, "is_open"), Output("is_data_loaded", "data"),
    Input('import_dataset', 'n_clicks_timestamp'), 
    Input(store_id, 'data'),
    State('upload-data', 'contents'), State('upload-data', 'filename'),  
    State("separator", "value"), State("nas", "value")
)
def update_storage(_, session_id, content, filename, separator, nas):
    if content is None: return (no_update, no_update, storage.get(session_id, False) != False)
    nas_val = nas.split(",")
    df = parse_contents(content, filename, separator, nas_val)
    if df is not None: 
        save_dataframe(session_id, df, filename)
        return (no_update, no_update, True)
    else : 
        return (["Unable to load the dataset, please check the format and separator."], True, False)
        

# 3)
# If loaded, show the columns in the dropdown

@app.callback(
    Output("div_columns", "style"), Output("columns", "options"),
    Input(store_id, "data"), Input("is_data_loaded", "data"), Input("are_columns_picked", "data")
)
def retrieve_columns(session_id, is_data_loaded, _):
    if not is_data_loaded : raise PreventUpdate
    df = get_dataframe(session_id)
    res = [{"label": col, "value": col} for col in list(df.columns)]
    return ({"display": "block"}, res)

# 4
# Keep only selected columns
@app.callback(Output("are_columns_picked", "data"), Input("validate_dataset", "n_clicks_timestamp"), State(store_id, "data"), State("is_data_loaded", "data"), State("columns", "value"))
def keep_selected_columns(_, session_id, is_data_loaded, columns):
    if not is_data_loaded: raise PreventUpdate
    if not storage.get(session_id, False): raise PreventUpdate
    if not columns or len(columns) < 1: raise PreventUpdate
    
    df = get_dataframe(session_id)
    df.drop(columns=columns, inplace=True)
    save_dataframe(session_id, df)
    return True

    
def parse_contents(contents, filename, separator, nas):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    print(separator)
    if 'csv' in filename.lower():
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=separator, na_values=nas)
    elif 'txt' in filename:
        df = pd.read_table(io.StringIO(decoded.decode('utf-8')), sep=separator, na_values=nas, engine="python")
    else :
        return None

    df.columns = df.columns.str.strip("#").str.upper().str.replace(" ", "_")
    return df

