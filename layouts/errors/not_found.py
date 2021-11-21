from app import app
import dash.html as html
import dash_bootstrap_components as dbc

layout = dbc.Container(
        [
            html.H1(["Page not found..",html.Img(src=app.get_asset_url('/images/loadcat.gif'), className="mb-4")]),
            html.Hr(),
            html.H4(
                "Sorry, this page doesn't exist. Please go back."
            ),
            
            html.H5(
                "If you think this is an error, contact us."
            ),
            dbc.Button("Return home", color="dark", href="/", class_name="mt-3"),
        ],
        className="mt-5 p-5 bg-light border rounded-3 text-center",
    )