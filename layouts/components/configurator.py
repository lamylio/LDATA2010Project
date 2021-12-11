from requirements import html, dbc, dcc

layout = dbc.Card([

    dbc.Spinner(id="loading_configurator", type="grow", fullscreen=True, fullscreen_style={"opacity": "0.5"}),
    dbc.CardHeader(html.H4("LDATA2010 - Graph visualisation")),

    dbc.CardBody([

        dbc.Button("Data importation", id="btn-dataset", color="dark", class_name="d-grid col-6 mx-auto mb-3", style={"opacity": 0.8}, outline=False),
        dbc.Alert(["Error while rendering the graph.", html.Br(), "Please check your options."], id="alert_configurator", is_open=False, duration=10000, color="danger", class_name="mx-auto text-center h2"),
        dbc.Accordion([
            dbc.AccordionItem([
                dbc.InputGroup([
                    dbc.InputGroupText("ID"),
                    dbc.Select(id="select_column_nodes_id", required=True, placeholder="Please import first"),
                ], id="input_column_nodes_id", class_name="p-0"),
                dbc.InputGroup([
                    dbc.InputGroupText("LABEL"),
                    dbc.Select(id="select_column_nodes_label", placeholder="Please import first")
                ], id="input_column_nodes_label", class_name="p-0 m-0"),

                dbc.InputGroup([
                    dbc.InputGroupText("SIZE"),
                    dbc.Select(id="select_column_nodes_size", placeholder="Please import first")
                ], id="input_column_nodes_size", class_name="p-0 m-0"),
                
                html.Br(),

                dbc.CardBody([
                    dbc.Checklist(
                        options=[
                            {"label": "Show labels", "value": 1},
                        ],
                        value=[1],
                        id="show_nodes_label_switch",
                        switch=True
                    ),
                ]),
                
                

            ], title="Options of nodes", item_id="accordion_nodes", style={"padding": "0 !important"}),

            dbc.AccordionItem([
                dbc.InputGroup([
                    dbc.InputGroupText("FROM"),
                    dbc.Select(id="select_column_edges_from", required=True, placeholder="Please import first"),
                ]),
                dbc.InputGroup([
                    dbc.InputGroupText("TO"),
                    dbc.Select(id="select_column_edges_to", required=True, placeholder="Please import first")
                ], id="input_column_edges", class_name="w-100" ),
            ], title="Options of edges", item_id="accordion_edges")

        ], start_collapsed=True, id="accordion_columns"),

    ]),

],id="configurator", outline=True, class_name="h-100")