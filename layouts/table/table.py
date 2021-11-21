from app import data
from dash import dcc
from dash import dash_table as dtb

import dash.html as html 

import dash_bootstrap_components as dbc


""" 
TODO :  
    Style the table
    Possibility to rename columns
    Don't show empty columns
    Register and save modifications (save button or auto?)
    Possibility to export in csv ?
"""

layout = dbc.Container(
    [
        dtb.DataTable(
            id="data-table", 
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in data.columns
            ],
            data=data.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 25
        )
        
    ],
    fluid=True
)

