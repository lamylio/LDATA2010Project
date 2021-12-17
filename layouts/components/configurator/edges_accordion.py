from requirements import dbc, dcc

layout = dbc.AccordionItem(title="Edges settings", children=[

    dbc.InputGroup([
        dbc.InputGroupText("ID"),
        dbc.Select(id="select_column_edges_id", required=True, placeholder="Please import first"),
    ], id="input_column_edges_id", class_name="p-0 my-1"),

    dbc.InputGroup([
        dbc.InputGroupText("FROM"),
        dbc.Select(id="select_column_edges_from", required=True, placeholder="Please import first"),
    ], class_name="w-100 my-1"),

    dbc.InputGroup([
        dbc.InputGroupText("TO"),
        dbc.Select(id="select_column_edges_to", required=True, placeholder="Please import first")
    ], class_name="w-100 my-1" ),

    dbc.InputGroup([
        dbc.InputGroupText("WEIGHT"),
        dbc.Select(id="select_column_edges_weight", required=True, placeholder="Please import first")
    ], class_name="w-100 mt-2 mb-1" ),

    dbc.Card(class_name="text-center p-1 my-2", outline=False, children=[
        dbc.Label("Opacity", class_name="bold"),
        dcc.Slider(
            min=10,
            max=100,
            value=90,
            step=10,
            tooltip={"placement": "bottom", "always_visible": True},
            id="input_edges_opacity"
        ),
        dbc.Label("Edges color", class_name="bold"),
        dbc.Input(
            type="color",
            id="input_edges_color",
            value="#000000",
            style={"border": "none"}
        ),
        
        dbc.Select(
            id="select_edges_color",
            options=[
                {"label": "Global", "value": False},
                {"label": "Starting node", "value": "from"},
                {"label": "Destination node", "value": "to"},
                {"label": "Both nodes", "value": "both"}
            ],
            value=False,
            class_name="",
        )
    ]),
    
    dbc.Card(class_name="text-center p-1 my-2", outline=False, children=[
        dbc.Label("Arrows", class_name="bold"),
        dbc.Checklist(
            options=[
                {"label": "From", "value": "from"},
                {"label": "Middle", "value": "middle"},
                {"label": "To", "value": "to"}
            ],
            inline=True,
            value=[],
            id="input_edges_arrows"
        )
    ])
])