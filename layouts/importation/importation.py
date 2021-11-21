import dash.html as html
from dash_bootstrap_components import Alert, Container

layout = Container(
    [    
        Alert(
            html.H1("Importation page! To be made.", style={"text-align": "center"}),
            is_open=True, style={"margin-top": "5em"}, color="danger"
        )
    ]
)