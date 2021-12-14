from requirements import dbc

layout = dbc.AccordionItem(title="Layouts", item_id="accordion_layouts", children=[
    
    dbc.RadioItems(
        id="input_layout_selector",
        className="btn-group-vertical w-100",
        inputClassName="btn-check w-100",
        labelClassName="btn btn-outline-primary btn-block rounded-0",
        labelCheckedClassName="active",
        
        options=[
            {"label": "Random", "value": 1},
            {"label": "Circular", "value": 2},
            {"label": "Spiral", "value": 3},
            # {"label": "Fruchterman", "value": 4},
            {"label": "Kamada-Kawai", "value": 5},
        ],
        value=1                        
    ),

])