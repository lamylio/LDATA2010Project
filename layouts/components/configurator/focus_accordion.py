from requirements import dbc, dcc

layout = dbc.AccordionItem(title="Focus group", children=[

    dbc.InputGroup([
        dbc.InputGroupText("ON"),
        dbc.Select(id="select_column_focus_on", required=True, placeholder="Please import first"),
    ], id="input_column_focus_on", class_name="p-0 my-1"),

    dbc.InputGroup([
        dbc.InputGroupText("VALUE"),
        dbc.Select(id="select_column_focus_value", required=True, placeholder="Select ON first"),
    ], id="input_column_focus_value", class_name="p-0 my-1"),

        
    dbc.Card([
        dbc.Row(class_name="mt-2",children=[
            dbc.Col([
                dbc.Switch(
                    id="show_focus_neighbors_of_neighbors",
                    label="Neighbors of neighbors",
                    value=False,
                    class_name="mx-2"
                ),
            ])
        ]),
    ])

])