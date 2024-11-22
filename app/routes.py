from app import app
from flask import render_template,jsonify,request,redirect,url_for
from app.forms import LoginForm,SalaForm
from app.models import queryGalen,querySala
from app.utils import todictionario,toSelect,tolist

@app.route('/')
def inicio():
	form=LoginForm()
	return render_template('inicio.html',form=form)
	
@app.route('/principal')
def principal():
	return render_template('base.html')

@app.route('/sala',methods=['POST','GET'])
def sala():
	form=SalaForm()
	if request.method=='POST':
		HC=form.HC.data
		TipoInter=form.Tipo_Intervecion.data
		upps=form.UPPS.data
		comple=form.COMPLEJIDAD.data
		dx1=form.DX1.data
		dx2=form.DX2.data
		interQ=form.IntervencionQ.data
		dxpos1=form.DX1POST.data
		dxpos2=form.DX2POST.data
		reintervencion=form.ReIntervecion.data
		cirujano=form.Cirujano.data
		anestesiologo=form.Anestesiologo.data
		instrumentista=form.InstrumentalistaI.data
		instrumentista2=form.InstrumentalistaII.data
		fech_ingre=form.FechaIngreso.data
		fi=fech_ingre.strftime('%Y-%m-%d')
		hora_ingre=form.HoraIngreso.data
		hi=str(hora_ingre.strftime('%H:%M'))

		fech_sali=form.FechaSalida.data
		fs=fech_sali.strftime('%Y-%m-%d')
		hora_sali=form.HoraSalida.data
		hs=str(hora_sali.strftime('%H:%M'))

		tiempoUso=form.TiempoUso.data
		derivado=form.Derivado.data
		financiamiento=form.Financiamiento.data
		observacion=form.Observacion.data
		responsable=form.Responsable.data
		situacion=form.Situacion.data
		data={'HC':str(HC),'Inter_Q':TipoInter,'UPPS':upps,'COMPLEJIDAD':comple,'DX1':dx1[:dx1.find("_")] if len(dx1)>5 else " ",
		'DX2':dx2[:dx2.find("_")] if len(dx2)>5 else " ",'INTQ':interQ[:interQ.find("_")] if interQ.find("_")>0 else "" ,'DX1POST':dxpos1[:dxpos1.find("_")] if len(dxpos1)>5 else " ",
		'DX2POST':dxpos2[:dxpos2.find("_")] if len(dxpos2)>5 else " ",'R_Interv':reintervencion,'Cirujano':cirujano,
		'Anestesiologo':anestesiologo,'InstrumentistaI':instrumentista,'InstrumentistaII':instrumentista2,'Fech_Ingre':fi,'Hora_Ingre':hi,
		'Fech_Sali':fs,'Hora_Sali':hs,'Tiempo_Uso':str(round(tiempoUso,2)),'Servicio_Deriva':derivado,'Financiamiento':financiamiento,'Observaciones':observacion,'Situacion':situacion,
		'Responsable':responsable}
		obj_sala=querySala()
		nro=obj_sala.InsertTable('Sala',data)		
		return redirect(url_for('sala'))
	else:
		obj_modelo=querySala()
		rows=obj_modelo.consultarTabla('UPSS')
		lista=tolist('Sala',50)	
		#llenando selects
		opciones=toSelect(rows,'Descripcion','Descripcion')
		form.UPPS.choices=opciones
		#complejidad
		rowsc=obj_modelo.consultarTabla('CCOMPLEJIDAD')
		opciones_complejidad=toSelect(rowsc,'Descripcion','Descripcion')
		form.COMPLEJIDAD.choices=opciones_complejidad

		#llenado financiamiento
		form.Financiamiento.choices=['SIS','PARTICULAR','SALUDPOL','SOAT']
		form.ReIntervecion.choices=['NO','SI']

		#llenar situacion
		form.Situacion.choices=['Suspendido','Ejecutado']
		form.Tipo_Intervecion.choices=['Programado','Emergencia']
		

		return render_template('sala.html',form=form,registros=lista)

@app.route('/llenardatospaciente',methods=['POST'])
def datosSala():
	hc=request.form.get('hc')
	obj_consulta=queryGalen()
	rows=obj_consulta.consultarTabla('Pacientes','NroHistoriaClinica',hc)
	dictinario=todictionario(rows,'PrimerNombre','ApellidoPaterno','ApellidoMaterno')	
	return jsonify(dictinario)


@app.route('/search',methods=['POST'])
def buscarempleado():
	valor=request.form.get('val')
	tabla=request.form.get('tabla')
	bd=request.form.get('bd')
	if bd=='GALEN':	
		obj_consulta=queryGalen()
		rows=obj_consulta.consultarTablaLike(tabla,'Nombres','ApellidoPaterno',valor)
		lista=[val.Nombres+' '+val.ApellidoPaterno+' '+val.ApellidoMaterno for val in rows]

	elif bd=='SALA':
		
		obj_sala=querySala()
		rows=obj_sala.consultarCIELike(tabla,'Detalle_Cie','Id_Cie',valor)
		lista=[val.Id_Cie+"_"+val.Detalle_Cie for val in rows]

	elif bd=='PROCEDIMIENTO':

		obj_sala=querySala()
		rows=obj_sala.consultarCIELike(tabla,'Id_Proced','Procedimiento',valor)

		lista=[val.Id_Proced+"_"+val.Procedimiento for val in rows]

	elif bd=='DERIVAR':
		obj_sala=querySala()
		rows=obj_sala.consultarCIELike(tabla,'Servicio','Servicio',valor)
		lista=[val.Servicio for val in rows]

	elif bd=='SALABUSQUEDA':
		obj_sala=querySala()
		rows=obj_sala.consultarCIELike(tabla,'HC','HC',valor)
		obj_galen=queryGalen()
		lista=[]
		for val in rows:
			rows_galen=obj_galen.consultarTabla('Pacientes','NroHistoriaClinica',val.HC)
			lista.append([val.Id_Sala,rows_galen[0].PrimerNombre+" "+ rows_galen[0].ApellidoPaterno+ " "+rows_galen[0].ApellidoMaterno,val.HC,val.Inter_Q,val.UPPS,val.COMPLEJIDAD,val.Fech_Ingre])

	return jsonify(lista)
	

@app.route('/urpa')
def urpa():
	obj_galen=queryGalen()
	obj_sala=querySala()
	rows=obj_sala.consultarLlenarUrpa()
	lista=[]
	for val in rows:		
		rowsDatos=obj_galen.consultarTabla('Pacientes','NroHistoriaClinica',val.HC)
		lista.append([val.Id_Sala,rowsDatos[0].PrimerNombre+" "+rowsDatos[0].ApellidoPaterno+" "+rowsDatos[0].ApellidoMaterno,val.HC,val.Fech_Ingre])
	return render_template('urpa.html',datos=lista)

@app.route('/fillselect',methods=['POST'])
def llenarlistas():
	tabla=request.form.get('tabla')
	condicion=request.form.get('condicion')
	bd=request.form.get('bd')
	condicionvalor=request.form.get('condicionvalor')
	if bd=='SALA':
		obj_sala=querySala()
		if condicionvalor.upper()=='EMERGENCIA':			
			rows=obj_sala.consultarLike(tabla,condicion,condicionvalor.strip(),1)
		else:
			rows=obj_sala.consultarLike(tabla,condicion,'emergencia',0)
		lista=[val.Descripcion for val in rows]
	return jsonify(lista)

@app.route('/deletesala',methods=['POST'])
def borrarSala():
	ideliminar=request.form.get('valor')
	obj_consulta=querySala()
	numero=obj_consulta.deleteSala(ideliminar)	
	return jsonify([numero])

@app.route('/modificarsala',methods=['POST'])
def EditarSala():
	tipointer=request.form.get('tipointer')
	upss=request.form.get('upss')
	complejidad=request.form.get('complejidad')
	codigo=request.form.get('codigo')
	
	data={'Inter_Q':tipointer,'UPPS':upss,'COMPLEJIDAD':complejidad}

	obj_consulta=querySala()
	nro=obj_consulta.ModificarTabla('Sala','Id_Sala',codigo,data)

	return jsonify([nro])

@app.route('/versala',methods=['POST'])
def VerSala():
	codigo=request.form.get('codigo')	

	obj_consulta=querySala()
	rows=obj_consulta.consultarTablaCondition('Sala','Id_Sala',codigo)
	for val in rows:
		rows_dx1=obj_consulta.consultarTablaCondition('Cie10','Id_Cie',val.DX1)
		rows_dx2=obj_consulta.consultarTablaCondition('Cie10','Id_Cie',val.DX2)
		IntervencionQ=obj_consulta.consultarTablaCondition('Procedimiento','Id_Proced',val.INTQ)
		rows_dx1post=obj_consulta.consultarTablaCondition('Cie10','Id_Cie',val.DX1POST)
		rows_dx2post=obj_consulta.consultarTablaCondition('Cie10','Id_Cie',val.DX2POST)

		datos=[{'HC':val.HC,'Inter_Q':val.Inter_Q,'UPPS':val.UPPS,'COMPLEJIDAD':val.COMPLEJIDAD,
		'DX1':rows_dx1[0].Detalle_Cie if rows_dx1 else "",'DX2':rows_dx2[0].Detalle_Cie if rows_dx2 else ""
		,'INTQ':IntervencionQ[0].Procedimiento if IntervencionQ else "",'DX1POST':rows_dx1post[0].Detalle_Cie if rows_dx1post else "",
		'DX2POST':rows_dx2post[0].Detalle_Cie if rows_dx2post else "",'CIRUJANO':val.Cirujano,'ANESTESIOLOGO':val.Anestesiologo,
		'INSTRUMENTISTAI':val.InstrumentistaI,'INSTRUMENTISTAII':val.InstrumentistaII,'FECHAINGRESO':val.Fech_Ingre } for val in rows]

	return jsonify(datos)