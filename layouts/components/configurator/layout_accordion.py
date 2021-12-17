from requirements import dbc

layout = dbc.AccordionItem(title="Layouts", item_id="accordion_layouts", children=[
    dbc.Card(class_name="text-center p-1 my-2", outline=False, children=[
        dbc.RadioItems(
            id="input_layout_selector",
            className="btn-group-vertical w-100 p-0",
            inputClassName="btn-check w-100 p-0",
            labelClassName="btn btn-outline-primary btn-block rounded-0 w-100",
            labelCheckedClassName="active",
            
            options=[
                {"label": "Circular", "value": 4},
                {"label": "Kamada-Kawai", "value": 6},
                {"label": "Spring (fruchterman)", "value": 1},
                {"label": "Spiral", "value": 3},
                # {"label": "Circular", "value": 2},
                # {"label": "Spectral (Laplacian)", "value": 5},
            ],
            value=4                  
        ),
    ])
    

])