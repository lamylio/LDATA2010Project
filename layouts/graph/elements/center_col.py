import dash.html as html
import dash_bootstrap_components as dbc

layout = dbc.Col(
    [
        dbc.Alert(
            html.H1("Graph page! To be made.", style={"text-align": "center"}),
            is_open=True, style={"margin-top": "5em"}, color="dark"
        )
    ],
    width=12, md=6, class_name="border h-100"
)