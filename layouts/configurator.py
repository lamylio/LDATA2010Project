from requirements import html, dbc
from .components import nodes_accordion, edges_accordion, layout_accordion

layout = dbc.Card(id="configurator", outline=True, class_name="h-100 overflow-auto", children=[

    dbc.Spinner([], id="loading_configurator", type="grow", fullscreen=True, fullscreen_style={"opacity": "0.5"}, show_initially=False),
    dbc.CardHeader(html.H4(["LDATA2010", html.Br(), "Graph visualisation"]), class_name="text-center"),
    dbc.Container([

        dbc.CardBody(children=[

            dbc.Button(html.H6("Data importation", className="m-0 p-1"), id="btn-dataset", color="dark", class_name="d-grid col-8 mx-auto mb-3 rounded-0", style={"opacity": 0.8}, outline=False),
            dbc.Alert([], id="alert_configurator", is_open=False, duration=15000, color="danger", class_name="mx-auto text-center h2"),
            
            dbc.Accordion(start_collapsed=True, flush=True, id="accordion_columns", children=[

                nodes_accordion,
                edges_accordion,
                layout_accordion,
                
                dbc.AccordionItem(title="Metrics", item_id="accordion_metrics", children= [
                    
                ])

            ]),

        ]),
    ], fluid=True),

])