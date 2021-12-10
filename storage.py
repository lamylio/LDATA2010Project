from app import dataframes, options, graphs
from pandas import DataFrame
from networkx import Graph

# %% Data dataframes
def dataframe_exists(session_id, type):
    return not dataframes.get(session_id, {}).get(type, {}).get("df", DataFrame()).empty

def get_dataframe(session_id, type):
    return dataframes.get(session_id, {}).get(type, {}).get("df", DataFrame()).copy() 

def get_dataframe_name(session_id, type):
    return dataframes.get(session_id, {}).get(type, {}).get("name", None)

def save_dataframe(session_id, dataframe, type, df_name=None):
    assert type in ["nodes", "edges"]
    if session_id not in dataframes: dataframes[session_id] = {"edges": {}, "nodes": {}}
    if session_id in dataframes and not df_name: df_name = dataframes.get(session_id, {}).get(type, {}).get("name", None)
    dataframes[session_id][type]["df"] = dataframe
    dataframes[session_id][type]["name"] = df_name



def settings_exists(session_id):
    return options.get(session_id, False) != False

def save_settings(session_id, settings):
    options[session_id] = settings

def get_settings(session_id):
    return options.get(session_id, {})



def graph_exists(session_id):
    return graphs.get(session_id, False) != False

def save_graph(session_id, graph):
    graphs[session_id] = graph

def get_graph(session_id):
    return graphs.get(session_id, Graph())