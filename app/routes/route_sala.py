from flask import Blueprint,render_template,redirect,url_for,request,jsonify,send_file
from flask_login import login_required
from app.forms import SalaForm
from app.models import queryGalen,querySala
from app.utils import todictionario,toSelect,tolist,validarcampos


sala_bp=Blueprint('salabp',__name__,url_prefix='/salabp')

@sala_bp.route('/sala',methods=['POST','GET'])
@login_required
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
		
		data={'HC':str(HC),'Inter_Q':TipoInter,'UPPS':upps,'COMPLEJIDAD':comple,'DX1':dx1[:dx1.find("_")] if len(dx1)>5 else " ",
		'DX2':dx2[:dx2.find("_")] if len(dx2)>5 else " ",'INTQ':interQ[:interQ.find("_")] if interQ.find("_")>0 else "" ,'DX1POST':dxpos1[:dxpos1.find("_")] if len(dxpos1)>5 else " ",
		'DX2POST':dxpos2[:dxpos2.find("_")] if len(dxpos2)>5 else " ",'R_Interv':reintervencion,'Cirujano':cirujano,
		'Anestesiologo':anestesiologo,'InstrumentistaI':instrumentista,'InstrumentistaII':instrumentista2,'Fech_Ingre':fi,'Hora_Ingre':hi,
		'Fech_Sali':fs,'Hora_Sali':hs,'Tiempo_Uso':tiempoUso,'Servicio_Deriva':derivado,'Financiamiento':financiamiento,'Observaciones':observacion,'Situacion':'Ejecutado',
		'Responsable':responsable}
		obj_sala=querySala()
		nro=obj_sala.InsertTable('Sala',data)		
		return redirect(url_for('salabp.sala'))
	else:
		obj_modelo=querySala()
		rows=obj_modelo.consultarTabla('UPSS')
		lista=tolist('Sala',50,'Fech_Ingre')	

		listaprogramado=tolist('CSUSPENDIDAS',50,'fechasuspencion')
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
		

		return render_template('sala.html',form=form,registros=lista,registrosprogramados=listaprogramado)

@sala_bp.route('/llenardatospaciente',methods=['POST'])
@login_required
def datosSala():
	hc=request.form.get('hc')
	obj_consulta=queryGalen()
	rows=obj_consulta.consultarTabla('Pacientes','NroHistoriaClinica',hc)
	dictinario=todictionario(rows,'PrimerNombre','ApellidoPaterno','ApellidoMaterno')	
	return jsonify(dictinario)


@sala_bp.route('/search',methods=['POST'])
@login_required
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
	

@sala_bp.route('/urpa')
@login_required
def urpa():
	obj_galen=queryGalen()
	obj_sala=querySala()
	rows=obj_sala.consultarLlenarUrpa()
	rowsURPA=obj_sala.consultarUrpa()
	lista=[]
	for val in rows:		
		rowsDatos=obj_galen.consultarTabla('Pacientes','NroHistoriaClinica',val.HC)
		lista.append([val.Id_Sala,rowsDatos[0].PrimerNombre+" "+rowsDatos[0].ApellidoPaterno+" "+rowsDatos[0].ApellidoMaterno,val.HC,val.Fech_Ingre])
	
	listaURPA=[]
	for val in rowsURPA:		
		rowsDatos=obj_galen.consultarTabla('Pacientes','NroHistoriaClinica',val.HC)
		listaURPA.append([val.Id_Sala,rowsDatos[0].PrimerNombre+" "+rowsDatos[0].ApellidoPaterno+" "+rowsDatos[0].ApellidoMaterno,val.HC,val.Fech_Ingre])
	
	return render_template('urpa.html',datos=lista,datosurpa=listaURPA)
	

@sala_bp.route('/fillselect',methods=['POST'])
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

@sala_bp.route('/deletesala',methods=['POST'])
@login_required
def borrarSala():
	ideliminar=request.form.get('valor')
	obj_consulta=querySala()
	numero=obj_consulta.deleteSala(ideliminar)	
	return jsonify([numero])

@sala_bp.route('/modificarsala',methods=['POST'])
@login_required
def EditarSala():
	tipointer=request.form.get('tipointer')
	upss=request.form.get('upss')
	complejidad=request.form.get('complejidad')
	codigo=request.form.get('codigo')
	
	data={'Inter_Q':tipointer,'UPPS':upss,'COMPLEJIDAD':complejidad}

	obj_consulta=querySala()
	nro=obj_consulta.ModificarTabla('Sala','Id_Sala',codigo,data)

	return jsonify([nro])


@sala_bp.route('/versala',methods=['POST'])
@login_required
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

@sala_bp.route('/llenarAnestesia',methods=['POST'])
def llenarSelectAnestesia():
	obj_consulta=querySala()
	rows=obj_consulta.consultarTabla('TANESTECIA')
	lista=[{'text':val.tipoA,'value':val.Id_TAnestecia} for val in rows]
	return jsonify(lista)

@sala_bp.route('/inserturpa',methods=['POST'])
@login_required
def InsertarUrpa():	
	datos={'Id_Sala':request.form.get('Id_Sala'),'T_ESPERA':request.form.get('tiempoespera'),'FECHAI':request.form.get('Fechaingreso'),
	'HORAI':request.form.get('Horaingreso'),'FECHAS':request.form.get('FehaSalida'),'HORAS':request.form.get('HoraSalida'),
	'T_PERMANENCIA':request.form.get('permanencia'),'DERIVAR':request.form.get('derivar'),'RESPONSABLE':request.form.get('responsable'),
	'Id_TAnestecia':request.form.get('tipoanestecia')}
	val=validarcampos(datos)
	obj_consulta=querySala()
	if val==1:
		rowstable=obj_consulta.consultarIdTable('URPA','Id_URPA')
		idUrpa=rowstable[0].idtabla+1 if rowstable else 1
		datos['Id_URPA']=idUrpa
		nro=obj_consulta.InsertTable('URPA',datos)
		return jsonify([nro])
	else:	
		return jsonify([val])

@sala_bp.route('/reportesala')
@login_required
def reportesala():
	return render_template('reporteSala.html')

@sala_bp.route('/programado',methods=['POST'])
@login_required
def cirugiaprogramado():
	obj_consulta=querySala()
	rows=obj_consulta.consultarTabla('MOTIVOSUSPENCION')
	lista=[{'value':val.idmotivo,'text':val.descripcion} for val in rows]
	return jsonify(lista)

@sala_bp.route('/insertsus',methods=['POST'])
@login_required
def insertsus():
	obj_consulta=querySala()
	codcie=request.form.get('Id_Cie')
	datos={'Id_Cie':codcie[:codcie.find('_')],'idmotivo':request.form.get('idmotivo'),
	'descripcionmotivo':request.form.get('descripcionmotivo'),
	'solucionp':request.form.get('solucionp'),'responsable':request.form.get('responsable'),
	'fechasuspencion':request.form.get('fechasuspencion'),'HC':request.form.get('HC')}
	val=validarcampos(datos);
	if val==1:
		nro=obj_consulta.InsertTable('CSUSPENDIDAS',datos)
		return jsonify([nro])
	else:
		return jsonify([val])

@sala_bp.route('/generarreportesala',methods=['GET'])
@login_required
def genreportesala():
	try:
		fechai=request.args.get('fechai')
		fechas=request.args.get('fechas')
		categoria=request.args.get('categoria')
		from app.reporteSala import generarReporteSala,generarReporteUrpa
		if categoria=='rsala':
			wb=generarReporteSala(fechai,fechas)
		elif categoria=='rurpa':
			wb=generarReporteUrpa(fechai,fechas)

		import tempfile
		with tempfile.NamedTemporaryFile(delete=False,suffix=".xlsx") as temp:
			wb.save(filename=temp.name)
		return send_file(temp.name,as_attachment=True,download_name=f'Reporte{categoria}.xlsx',mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	except Exception as e:
		print(e)
	
	

	