
import base64
import io

import pandas as pd
from app import app, store_data
from layouts.requirements import dcc, html, dbc, Input, Output, State, PreventUpdate

layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ', html.A('Select Files', style={"cursor": "pointer"}, className="font-bold")
        ]),
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
    )
])

# Show the name of the dataset, or that none as been imported
@app.callback(Output("data_name", "children"), Output("upload-data", "children"), Input("upload-data", "filename"), Input("offcanvas-dataset", "is_open"), State(store_data, "data"))
def show_uploaded_filename(filename, is_open, store):
    if not is_open: raise PreventUpdate
    
    up_default = html.Div([
        'Drag and Drop or ', html.A('Select Files', style={"cursor": "pointer"}, className="font-bold")
    ])
    
    if filename: return [filename, f"File uploaded: {filename}"]
    data = store or {}
    return [data.get("name", "Data not yet imported."), up_default]

@app.callback(
    Output("columns", "options"), Output("columns", "value"),
    Input('upload-data', 'contents'), State('upload-data', 'filename'), State("separator", "value"), State("nas", "value")
)
def retrieve_columns(content, filename, separator, nas):
    if content is None : raise PreventUpdate
    nas_val = nas.split(',')
    df = parse_contents(content, filename, separator, nas_val)
    res = [{"label": col, "value": col} for col in list(df.columns)]
    return res, [col for col in list(df.columns)]

# Retrieve the data from the upload button, and save it in json to the storage
@app.callback(
    Output(store_data, "data"), Input('validate', 'n_clicks_timestamp'), 
    State(store_data, "data"),
    State('upload-data', 'contents'), State('upload-data', 'filename'),  
    State("separator", "value"), State("columns", "value"), State("nas", "value")
)
def update_storage(_, store, content, filename, separator, columns, nas):
    if content is None: raise PreventUpdate
    data = store or {}
    nas_val = nas.split(",")
    df = parse_contents(content, filename, separator, nas_val)[columns]
    data["json"] = df.to_json(orient="split")
    data["name"] = filename
    return data

    
def parse_contents(contents, filename, separator, nas):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    print(separator)
    try:
        if 'csv' in filename.lower():
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=separator, na_values=nas)
        elif 'txt' in filename:
            df = pd.read_table(io.StringIO(decoded.decode('utf-8')), sep=separator, na_values=nas, engine="python")
    except Exception as e:
        print(e)
        df = pd.DataFrame()

    df.columns = df.columns.str.strip("#").str.upper().str.replace(" ", "_")
    return df

