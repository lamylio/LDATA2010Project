from app import cache

def hex_to_rgba(hex, opacity):
    hex = hex.lstrip("#")
    rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba{(*rgb, opacity)}"

def constrasting_text(str_rgba: str):
    rgba = str_rgba.lstrip("rgba(").lstrip(")")
    r,g,b,a = rgba.split(",")
    red, green, blue = int(r), int(g), int(b)
    if (red*0.299 + green*0.587 + blue*0.114) > 186: return "#000000" 
    else: return "#ffffff"

# import_callbacks.py

def parse_file_contents(contents, filename, separator, nas):
    from pandas import read_csv, read_table
    from base64 import b64decode
    from io import StringIO
    _, content_string = contents.split(',')
    decoded = b64decode(content_string)
    if 'csv' in filename.lower():
        df = read_csv(StringIO(decoded.decode('utf-8')), sep=separator, na_values=nas)
    elif 'txt' in filename:
        df = read_table(StringIO(decoded.decode('utf-8')), sep=separator, na_values=nas, engine="python")
    else :
        return None

    df.columns = df.columns.str.strip("#").str.strip("@").str.upper().str.replace(" ", "_")
    return df

# graph_callbacks.py

@cache.memoize()
def populate_nodes(df, column):
    return df[column].drop_duplicates().dropna()

@cache.memoize()
def populate_edges(df, col_from, col_to, nodes):
    dfc = df[[col_from, col_to]].drop_duplicates()
    edges_clean = [(fr, to) for fr, to in zip(
        dfc[col_from],
        dfc[col_to]
    ) if fr in nodes and to in nodes]
    return edges_clean

@cache.memoize()
def isolate_by_id(df, column_id, column_to_isolate):
    return df[[column_id, column_to_isolate]].set_index(column_id)

def layout_value_to_function(value):
    import networkx.drawing.layout as nxl
    layouts = {
        1: nxl.random_layout,
        2: nxl.circular_layout,
        3: nxl.spiral_layout,
        4: nxl.shell_layout,
        5: nxl.spectral_layout,
        6: nxl.kamada_kawai_layout
    }
    for k,v in layouts.items():
        if k == value: return v

    return nxl.kamada_kawai_layout

def graph_alert_message(message=""):
    from dash.html import Br, B, I
    return [B("Error while rendering the graph"), Br(), I(message), Br(), "Please check your options."]