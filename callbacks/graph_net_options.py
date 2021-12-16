from app import app
from utils import hex_to_rgba

def get_all_options(session_id, settings):
    return {
        "height": "100%",
        "width":  "100%",
        **get_nodes_edges_groups(session_id, settings),
        **get_others(session_id, settings)
    }


def get_nodes_edges_groups(session_id, settings):
    if app.server.debug: print(session_id, "> update_graph > to network > net_options_nodes")
    net_options_nodes = {
        "color": hex_to_rgba(settings.get('NODES_COLOR', '#000000'), int(settings.get('NODES_OPACITY', 100))/100),
        "font": {
            "color": "#000000", # constrasting_text(hex_to_rgba(settings.get('NODES_COLOR', '#000000'), int(settings.get('NODES_OPACITY', 100))/100))
            "vadjust": -5
        },
        "shape": "dot",
        "scaling": {
            "min": 5,
            "max": 15,
            "label": {
                "enabled": True,
                "min": 10,
                "max": 20
            }
        }
    }
    
    if app.server.debug: print(session_id, "> update_graph > to network > net_options_edges")
    net_options_edges = {
        "arrows": {
            "from": {
                "enabled": "from" in settings.get("EDGES_ARROWS", []) or False,
                "scaleFactor": 1.1
            },
            "middle": {
                "enabled": "middle" in settings.get("EDGES_ARROWS", []) or False,
                "scaleFactor": 1.1
            },
            "to": {
                "enabled": "to" in settings.get("EDGES_ARROWS", []) or False,
                "scaleFactor": 1.1
            }
        },
        "arrowStrikethrough": False,
        "color":{
            **(
                {"color": settings.get('EDGES_COLOR', '#000000'),
                "highlight": settings.get('EDGES_COLOR', '#000000'),
                "hover": settings.get('EDGES_COLOR', '#000000')},
                {}
            )[settings.get("EDGES_COLOR_INHERIT", "false") != "false"],
            "opacity": int(settings.get('EDGES_OPACITY', 30)) / 100,
            "inherit": settings.get("EDGES_COLOR_INHERIT", "false")
        },
        "font": {
            "size": 11
        },
        "scaling": {
            "min": 3,
            "max": 15,
        },
        "smooth": {
            "type": "continuous",
            "forceDirection": "none",
            "roundness": 0.1
        }
    }

    net_options_groups = {
        "@NOT_FOCUS": net_options_nodes,
    }

    return dict(nodes=net_options_nodes, edges=net_options_edges, groups=net_options_groups)

def get_others(session_id, settings):
    if app.server.debug: print(session_id, "> update_graph > to network > net_options_interactions")
    net_options_interactions = {
        "keyboard": True,
        "multiselect": False,
        "navigationButtons": False
    }
    
    if app.server.debug: print(session_id, "> update_graph > to network > net_options_physics")
    net_options_physics = {
        "stabilization": False,
        "timestep": 0,
        "adaptiveTimestep": False
    }
    
    if app.server.debug: print(session_id, "> update_graph > to network > net_options_manipulation")
    net_options_manipulation = {
        "enabled": True
    }
    
    return dict(interaction=net_options_interactions, manipulation=net_options_manipulation, physics=net_options_physics)