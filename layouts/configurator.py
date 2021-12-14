from requirements import html, dbc
from .components import nodes_accordion, edges_accordion, layout_accordion

layout = dbc.Card(id="configurator", outline=True, class_name="h-100 overflow-auto", children=[

    dbc.Spinner([], id="loading_configurator", type="default", fullscreen=True, fullscreen_style={"opacity": "0.5"}, show_initially=False),
    dbc.CardHeader(html.H4("LDATA2010 - Graph visualisation")),
    dbc.Container([

        dbc.CardBody(children=[

            dbc.Button("Data importation", id="btn-dataset", color="dark", class_name="d-grid col-6 mx-auto mb-3 rounded-0", style={"opacity": 0.8}, outline=False),
            dbc.Alert(["Error while rendering the graph.", html.Br(), "Please check your options."], id="alert_configurator", is_open=False, duration=15000, color="danger", class_name="mx-auto text-center h2"),
            
            dbc.Accordion(class_name="overflow-auto", start_collapsed=True, flush=True, id="accordion_columns", children=[

                nodes_accordion,
                edges_accordion,
                layout_accordion,
                
                dbc.AccordionItem(title="Metrics", item_id="accordion_metrics", children= [
                    
                ])

            ]),

        ]),
    ], fluid=True),

])