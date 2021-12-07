from app import col_dataset_name
from pandas import DataFrame

# %% Data storage

# {session_id: {nodes: {col : val}, edges: {col: val}}}
storage = {}

def blank_storage(session_id):
    if session_id not in storage: storage[session_id] = {"edges": {}, "nodes": {}}

def dataframe_exists(session_id, type):
    assert type in ["nodes", "edges"]
    return storage.get(session_id, {}).get(type, False) != False

def get_dataframe(session_id, type):
    assert type in ["nodes", "edges"]
    d = storage.get(session_id, {}).get(type, {}).copy() 
    if col_dataset_name in d : del d[col_dataset_name]
    return DataFrame.from_dict(d)

def get_dataframe_name(session_id, type):
    assert type in ["nodes", "edges"]
    return storage.get(session_id, {}).get(type, {}).get(col_dataset_name, None)

def save_dataframe(session_id, dataframe, type, df_name=None):
    assert type in ["nodes", "edges"]
    if session_id not in storage: storage[session_id] = {"edges": {}, "nodes": {}}
    if session_id in storage and not df_name: df_name = storage.get(session_id, {}).get(type, {}).get(col_dataset_name, "Unknown name")
    storage[session_id][type] = dataframe.to_dict(orient="list")
    storage[session_id][type][col_dataset_name] = df_name