from dash import Dash
from dash import html,dcc
from app.models import queryHIS
import pandas as pd

def init_dash_app(server):
	obj_his=queryHIS()
	columnas,rows=obj_his.consultarAtenciones()	
	dash_app = Dash(__name__,server=server,url_base_pathname='/dash/')
	rows=[[val[0],val[1]] for val in rows]
	df=pd.DataFrame(rows,columns=columnas)
	
    # Configura el layout de la aplicación Dash
	dash_app.layout = html.Div([      
        dcc.Graph(
            id='example-graph',
            figure={
                	'data': [
                    			{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    			{'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'NYC'},
                			],
               		'layout': {
                   				'title': 'Ejemplo de Gráfico Dash'
                				}
            		}
        )
    ])
	return dash_app

