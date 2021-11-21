import dash.html as html
import dash_bootstrap_components as dbc

layout = html.Div(
    [    
        dbc.Alert(
            html.H1("Importation page! To be made.", style={"text-align": "center"}),
            is_open=True, style={"margin-top": "5em"}, color="danger"
        )
    ]
)