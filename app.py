from dash import Dash
from dash_bootstrap_components.themes import LITERA

# %% Create the app
app = Dash(__name__, external_stylesheets=[LITERA])
server = app.server

# %% Variable storing. NOTE: data defined as such is temporary

import pandas as pd
data = pd.read_table(
    "data/INTERACTIONS.tab3.txt", 
    na_values=["-", "-|-", "-|-|-", "-|-|-|-", "-|-|-|-|-"], 
    low_memory=False
)
data.columns = data.columns.str.strip("#").str.upper().str.replace(" ", "_")
data = data.head(50)
data.dropna(thresh=len(data.index)/2, axis=1, inplace=True)