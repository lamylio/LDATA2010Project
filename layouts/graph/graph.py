import dash.html as html
import dash_bootstrap_components as dbc

from layouts.graph.elements import left_col, center_col, right_col

layout = html.Div(
    [    
        dbc.Row(
            [
                left_col.layout,
                center_col.layout,
                right_col.layout
            ],
        class_name="h-100", align="center")
    ],
    className="h-100"
)