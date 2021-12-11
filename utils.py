def parse_file_contents(contents, filename, separator, nas):
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

    df.columns = df.columns.str.strip("#").str.strip("@").str.upper().str.replace(" ", "_")
    return df

# def create_nodes(column_nodes_id, column_nodes_label, session_id):
#     if not column_nodes_id or not column_nodes_label: raise PreventUpdate
#     df = DataFrame()
#     while df.empty: df = get_dataframe(session_id, "nodes")
#     df_unique = df[[column_nodes_id, column_nodes_label]].drop_duplicates(subset=[column_nodes_id])
#     nodes = dict(id=df_unique[column_nodes_id], label=df_unique[column_nodes_label])
#     # nodes = [{"id": id, "label": str(label)} for id, label in set(zip(df[column_nodes_id], df[column_nodes_label]))]
#     return nodes


# def create_edges(column_edges_from, column_edges_to,  session_id):
#     if not column_edges_from or not column_edges_to: raise PreventUpdate
#     df = DataFrame()
#     while df.empty: df = get_dataframe(session_id, "edges")
#     df_unique = df[[column_edges_from, column_edges_to]].drop_duplicates()
#     # nodes = dict(
#     #     id=[zip(df_unique[column_edges_from], df_unique[columns]], 
#     #     from=df_unique[column_edges_from],
#     #     to=
#     # )
#     edges = [{"id": f"{n_from}-{n_to}", "from": n_from, "to": n_to} for n_from, n_to in set(zip(df[column_edges_from], df[column_edges_to]))]
#     return edges