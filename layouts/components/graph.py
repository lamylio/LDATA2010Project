from app import app, store_graph

from layouts.requirements import html

import visdcc

layout = html.Div(
    [    
        visdcc.Network(id="net", options={"height": "1000px", "width": "100%", "nodes": {"color": "black"}, "edges": {"color": "red"}}, data={
            'nodes':[
                {'id': 1, 'label': "Node 1"},
                {'id': 2, 'label': 'Node 2'},
                {'id': 3, 'label': 'Node 3'},
                {'id': 4, 'label': 'Node 4'},
                {'id': 5, 'label': 'Node 5'},
                {'id': 6, 'label': 'Node 6'}                    
            ],
           'edges':[
                {'id':'1-2', 'from': 1, 'to': 2} ,
                {'id':'1-3', 'from': 1, 'to': 3} ,
                {'id':'1-4', 'from': 1, 'to': 4} ,
                {'id':'1-5', 'from': 1, 'to': 5} ,
                {'id':'1-6', 'from': 1, 'to': 6} ,
                {'id':'2-4', 'from': 2, 'to': 4} ,
            ]
           }
        )
    ],
    className="h-100 position-absolute"
)