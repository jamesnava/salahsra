from dash import Dash
from dash import html,dcc,Input,Output,callback
import dash_autocomplete as aut
from app.models import queryHIS
import pandas as pd
import plotly.express as px

def init_dash_app(server):
	obj_his=queryHIS()
	columnas,rows=obj_his.consultarAtenciones()
	
	dash_app = Dash(__name__,server=server,url_base_pathname='/dash/')
	rows=[[val[0],val[1],val[2],val[3],val[4]] for val in rows]
	df=pd.DataFrame(rows,columns=columnas)

	fig=px.line(df,x='Fecha_Atencion',y='cantidad')

	options=df['DatosP'].unique().tolist()
	options_servicio=df['Id_Ups'].unique().tolist()
	
	dash_app.layout = html.Div([html.H1("Producción por Medico"),html.Div([dcc.Dropdown(id='medico',options=[{'label': i, 'value': i} for i in options],value=None,multi=False
    ,style={'width': '40%'},),
    dcc.Dropdown(id='servicio',options=[{'label': i, 'value': i} for i in options_servicio],value=None,multi=False,style={'width': '40%'},),
    dcc.RadioItems(['Anual','Mensual','diario'],'diario',inline=True,id='frequencia',style={'color': 'MediumTurqoise', 'font-size': 20})],style={'display':'flex'}),
    dcc.Graph(id='barra')],style={'display':'flex','flex-direction':'column','gap':'20px','justify-content':'space-between'})

	@dash_app.callback(Output('servicio','options'),[Input('medico','value')])
	def update_dropdowns(valor):
		df_filter=df[df['DatosP']==valor]
		return [{'label':i,'value':i} for i in df_filter['Id_Ups'].unique()]

	@dash_app.callback(Output('barra','figure'),[Input('medico','value'),Input('servicio','value'),Input('frequencia','value')])
	def update_output_div(medico,servicio,frecuencia):	

    	# Filtrar los datos según el valor de búsqueda
		filtered_df = df[(df['DatosP']==medico) & (df['Id_Ups']==servicio)]
		filtered_df.set_index('Fecha_Atencion',inplace=True)
		filtered_df=filtered_df.sort_values('Fecha_Atencion')
		filtered_df.index=pd.to_datetime(filtered_df.index)

		if frecuencia=='Anual':
			df_final=filtered_df.resample('YE').sum()
		elif frecuencia=='Mensual':
			df_final=filtered_df.resample('ME').sum()
		else:
			df_final=filtered_df

    	# Crear el gráfico con los datos filtrados
		fig = px.line(df_final, x=df_final.index, y="cantidad",title=f'Responsable: {medico}')
		fig.update_layout(template='plotly_dark')
		return fig

	return dash_app

