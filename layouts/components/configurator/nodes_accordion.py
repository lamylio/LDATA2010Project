from requirements import dbc, dcc

layout = dbc.AccordionItem(title="Nodes settings", item_id="accordion_nodes", style={"padding": "0 !important"}, children=[
    dbc.InputGroup([
        dbc.InputGroupText("ID"),
        dbc.Select(id="select_column_nodes_id", required=True, placeholder="Please import first"),
    ], id="input_column_nodes_id", class_name="p-0 my-1"),
    dbc.InputGroup([
        dbc.InputGroupText("LABEL"),
        dbc.Select(id="select_column_nodes_label", placeholder="Please import first")
    ], id="input_column_nodes_label", class_name="p-0 my-1"),

    dbc.InputGroup([
        dbc.InputGroupText("SIZE"),
        dbc.Select(id="select_column_nodes_size", placeholder="Please import first", value="@NONE")
    ], id="input_column_nodes_size", class_name="p-0 my-1"),
    
    
    dbc.Card(class_name="text-center p-1 my-2 d-none", outline=False, children=[
        dbc.Label("Position", class_name="bold"),

        dbc.Checklist(
            options=[
                {"label": "Fixed x", "value": "x"},
                {"label": "Fixed y", "value": "y"}
            ],
            inline=True,
            value=[],
            id="input_fixed_x_y"
        )
    ]),
    
    dbc.Card(class_name="text-center p-1 my-2", outline=False, children=[
        dbc.Label("Opacity", class_name="bold"),
        dcc.Slider(
            min=10,
            max=100,
            value=90,
            step=10,
            tooltip={"placement": "bottom", "always_visible": True},
            id="input_nodes_opacity"
        ),
        dbc.Label("Nodes color", class_name="bold"),
        dbc.Input(
            type="color",
            id="input_nodes_color",
            value="#000000",
            style={"border": "none"}
        ),
    ]),
    
    dbc.Card([
        dbc.Row(class_name="text-center mt-2",children=[
            dbc.Col([
                dbc.Label("Show labels"),
                dbc.Switch(
                    value=False,
                    id="show_nodes_label_switch",
                    class_name="mx-auto",
                    input_class_name="p-0 mx-auto",
                    label_class_name="p-0 mx-auto"
                ),
            ]),
            dbc.Col(class_name="text-center", children=[
                dbc.Label("Show selected"),
                dbc.Switch(
                    value=False,
                    id="show_selected_node_switch",
                    class_name="mx-auto",
                    input_class_name="p-0 mx-auto",
                    label_class_name="p-0 mx-auto"
                ),
            ]),
        ]),
    ])
    
])