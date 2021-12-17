from requirements import html, dbc

layout = dbc.AccordionItem(title="Metrics", item_id="accordion_metrics", class_name="placeholder-wave", children= [
    html.P(["Graph assortativity: ", html.Span(html.Span(className="placeholder col-1"), id="graph_assortativity")]),
    html.P(["Graph transitivity ", html.Span(html.Span(className="placeholder col-1"), id="graph_transitivity")]),
    html.P(["Average node connectivity: ", html.Span(html.Span(className="placeholder col-1"), id="graph_connectivity")]),
    html.P(["Average clustering: ", html.Span(html.Span(className="placeholder col-1"), id="graph_avg_clustering")]),
    # html.P(["Generalized degree: ", html.Span(id="graph_generalized_degree")]),
    html.Hr(),
])