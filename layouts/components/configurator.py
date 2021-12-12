from requirements import html, dbc, dcc

layout = dbc.Card([

    dbc.Spinner(id="loading_configurator", type="grow", fullscreen=True, fullscreen_style={"opacity": "0.5"}),
    dbc.CardHeader(html.H4("LDATA2010 - Graph visualisation")),
    dbc.Container([

        dbc.CardBody([

            dbc.Button("Data importation", id="btn-dataset", color="dark", class_name="d-grid col-6 mx-auto mb-3 rounded-0", style={"opacity": 0.8}, outline=False),
            dbc.Alert(["Error while rendering the graph.", html.Br(), "Please check your options."], id="alert_configurator", is_open=False, duration=15000, color="danger", class_name="mx-auto text-center h2"),
            dbc.Accordion([

                dbc.AccordionItem(title="Options of data", item_id="accordion_nodes", style={"padding": "0 !important"}, children=[
                    dbc.Card([
                        dbc.CardHeader("Nodes settings"),
                        dbc.CardBody([
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

                            dbc.Row(class_name="text-center",children=[
                                dbc.Col([
                                    dbc.Label("Show labels"),
                                    dbc.Switch(
                                        value=False,
                                        id="show_nodes_label_switch"
                                    ),
                                ]),
                                dbc.Col([
                                    dbc.Label("Nodes color"),
                                    dbc.Input(
                                        type="color",
                                        id="input_nodes_color",
                                        value="#000000",
                                        style={}
                                    ),
                                ])
                            ])
                            


                        ])
                    ]),

                    dbc.Card([
                        dbc.CardHeader("Edges settings"),
                        dbc.CardBody([

                            dbc.InputGroup([
                                dbc.InputGroupText("FROM"),
                                dbc.Select(id="select_column_edges_from", required=True, placeholder="Please import first"),
                            ]),

                            dbc.InputGroup([
                                dbc.InputGroupText("TO"),
                                dbc.Select(id="select_column_edges_to", required=True, placeholder="Please import first")
                            ], id="input_column_edges", class_name="w-100" ),
                        ])
                    ])
                ]),

                dbc.AccordionItem(title="Layouts", item_id="accordion_layouts", children=[
                    
                    dbc.RadioItems(
                        id="input_layout_selector",
                        className="btn-group-vertical w-100",
                        inputClassName="btn-check w-100",
                        labelClassName="btn btn-outline-primary btn-block rounded-0",
                        labelCheckedClassName="active",
                        
                        options=[
                            {"label": "Free", "value": 1},
                            {"label": "Circular", "value": 2},
                            {"label": "Spiral", "value": 3},
                            {"label": "Fruchterman", "value": 4},
                            {"label": "Kamada-Kawai", "value": 5},
                        ],
                        value=1                        
                    ),

                ])

            ], start_collapsed=True, id="accordion_columns"),

        ]),
    ], fluid=True),

],id="configurator", outline=True, class_name="h-100")