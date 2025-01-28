from flask import Blueprint,render_template,request
from flask_login import login_required
from app.models import queryHIS

medico_bp=Blueprint('medico',__name__,url_prefix='/medico')

@medico_bp.route('/estadisticamedico')
@login_required
def estadisticomedico():
	return render_template('medico/estadisticamedico.html')

@medico_bp.route('/configuracion')
@login_required
def confgmedico():
	return render_template('medico/configuracionmedico.html')

@medico_bp.route('/updateData',methods=['POST'])
@login_required
def updatedata():
	file=request.files.get('filename')
	identificador=request.form.get('identificador')
	import pandas as pd
	obj_his=queryHIS()
	
	cantidad=0
	if identificador=='btnupdatetrama':
		data=pd.read_csv(file,sep=',')
		data=data.fillna('')
		diccionario=data.to_dict(orient='records')
		for valores in diccionario:
			rows=obj_his.consultarAtencionCampos(valores['Id_Cita'],valores['Codigo_Item'],valores['Fecha_Atencion'],valores['Lote'])		
			if not rows:
				nro=obj_his.InsertTable('TRAMA',valores)
				if nro:
					cantidad=cantidad+1				
			
	elif identificador=='btnupdatepersonal':
		data=pd.read_csv(file,sep=',',encoding='latin1')		
		data=data.fillna('')
		diccionario=data.to_dict(orient='records')
		for valores in diccionario:
			rows=obj_his.consultarAtencionParametro('MAESTRO_PERSONAL','Id_Personal',valores['Id_Personal'])
			if not rows:				
				nro=obj_his.InsertTable('MAESTRO_PERSONAL',valores)
				if nro:
					cantidad=cantidad+1

	return [cantidad]

