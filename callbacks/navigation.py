from dash import Input, Output, dcc
from app import app, data
import layouts

# %% Navigation callback to render appropriate page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    path = pathname[1:]

    if path in ["", "/", "home", "graph"]:
        if data is None: 
            return dcc.Location("no_data_redirect", href="/import", refresh=True)
            # return layouts.importation
        return layouts.graph

    elif path in ["import", "importation"]:
        return layouts.importation

    elif path in ["table", "data"]:
        return layouts.table

    return layouts.errors.not_found