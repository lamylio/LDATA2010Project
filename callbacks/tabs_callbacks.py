from pkgutil import get_data
from app import app, store_id, store_settings, store_graph
from storage import dataframe_exists, get_dataframe, get_graph, graph_exists
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
    # Output("network", "data"),
    # Output("network", "options"),
    Input(store_graph, "data"),
    Input("tabs", "active_tab"),
    State("tabs", "class_name")
)
def draw_network_tab(store_graph, active_tab, tabs_class):
    if not store_graph: raise PreventUpdate()
    if tabs_class == "d-none": raise PreventUpdate()
    if active_tab != "network": raise PreventUpdate()
    data = store_graph.get("data")
    options = store_graph.get("options")
    # return data, options
    return (
        Network(id="network", options=options, data=data, moveTo={"position": {"x": 0, "y": 0, "scale": 0.5}}, style={"height": "96vh", "width": "100%"}),
    )

@app.callback(
    Output("tab_matrix", "children"),
    Output("loading_adjacency", "children"),
    State(store_id, "data"),
    Input("tabs", "active_tab"),
    State("tabs", "class_name"),
    Input(store_graph, "data"),
    Input(store_settings, "data"),
)
def draw_adjacency_tab(session_id, active_tab, tabs_class, store_graph, _):
    if not graph_exists(session_id): raise PreventUpdate
    if active_tab != "matrix": raise PreventUpdate
    if tabs_class == "d-none": raise PreventUpdate
    from plotly.express import imshow
    from networkx import to_numpy_matrix 
    graph = get_graph(session_id)
    nodes = store_graph.get("data").get("nodes")
    labels = [node.get("label") or node.get("id") for node in nodes]
    heat = imshow(to_numpy_matrix(graph), x=labels, y=labels, color_continuous_scale="blues",zmin=0, zmax=1, labels={"x": "Nodes", "y": "Nodes", "color": "Neighbours = 1"})
    return [
        dbc.Spinner(html.Div(), id="loading_adjacency", color="primary", size="lm", show_initially=False), 
        dcc.Graph(id="fig_heatmap", figure=heat, className="d-flex mx-auto text-center", responsive=True, config={"fillFrame": True})
    ], html.Div()


@app.callback(
    Output("hist_1", "children"),
    State(store_id, "data"),
    Input("tabs", "active_tab"),
    State("tabs", "class_name"),
    Input(store_graph, "data"),
    Input(store_settings, "data"),
)
def draw_hist_one(session_id, active_tab, tabs_class, store_graph, _):
    if not graph_exists(session_id): raise PreventUpdate()
    if active_tab != "matrix": raise PreventUpdate()
    if tabs_class == "d-none": raise PreventUpdate()
    from plotly.express import bar
    from collections import Counter
    graph = get_graph(session_id)
    degree_seq = sorted([d for _, d in graph.degree()], reverse=True) 
    degreeCount = Counter(degree_seq)
    deg, cnt = zip(*degreeCount.items())
    heat = bar(x=deg, y=cnt, labels={"x": "Degree", "y": "Nodes count"})
    return dcc.Graph(id="fig_degree_bar", figure=heat)

@app.callback(
    Output("df_nodes", "columns"),
    Output("df_nodes", "data"),
    Input(store_id, "data"),
    Input("all_loaded", "data")
)
def datatable_nodes(session_id, _):
    if not dataframe_exists(session_id, "nodes"): raise PreventUpdate()
    df = get_dataframe(session_id, "nodes")
    columns = [{"name": c, "id": c, 'deletable': True} for c in df.columns]
    data = df.to_dict("records")
    return columns, data

@app.callback(
    Output("df_edges", "columns"),
    Output("df_edges", "data"),
    Input(store_id, "data"),
    Input("all_loaded", "data")
)
def datatable_edges(session_id, _):
    if not dataframe_exists(session_id, "edges"): raise PreventUpdate()
    df = get_dataframe(session_id, "edges")
    columns = [{"name": c, "id": c, 'deletable': True} for c in df.columns]
    data = df.to_dict("records")
    return columns, data

