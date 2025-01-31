from flask import Blueprint,render_template,request,g,abort,flash, redirect,url_for,jsonify
from flask_login import login_required,current_user
from functools import wraps
from app.models import querySala
from app.modelos.modconfiguraciones.queryconfiguracion import MConfiguraciones 


configuracion_bp=Blueprint('cfg',__name__,url_prefix='/cfg')
bd_current='salap'

@configuracion_bp.before_request
def cargar_usuario():
	if current_user.is_authenticated:
		obj_sala=querySala()
		g.user=obj_sala.Cargarusuario('iduser',current_user.id)

def check_permissions(*required_role):
	def decorator(f):		
		@wraps(f)
		def decorated_function(*args,**kwargs):
						
			obj_sala=querySala()			
			rows=obj_sala.ConsultaRoles(current_user.id)
			lista_roles=[val.Nombre for val in rows]			
			if not set(lista_roles).intersection(set(required_role)):
				flash('No tienes lo permiso suficientes para acceder a esta ruta!!','warning')
				return redirect(url_for('main.principal'))				
			return f(*args,**kwargs)
		return decorated_function
	return decorator

@configuracion_bp.route('/config')
@login_required
@check_permissions('ADMINISTRADOR')
def configuracion():
	return render_template('config/configuraciongeneral.html')

@configuracion_bp.route('/userconfig')
@login_required
@check_permissions('ADMINISTRADOR')
def userconf():
	return render_template('config/usermenu.html')


@configuracion_bp.route('/listarpersonal')
@login_required
@check_permissions('ADMINISTRADOR')
def listarpersonal():
	obj_consulta=MConfiguraciones(bd_current)
	sql='SELECT * FROM PERSONA'
	
	rows=obj_consulta.consultaPersonales(sql)
	data=[{'Dni':val.Dni,'NOMBRES':val.NOMBRES,'APELLIDOS':val.APELLIDOPATERNO+' '+val.APELLIDOMATERNO} for val in rows]
	html=render_template('config/personal.html')

	return jsonify({'html':html,'data':data})


@configuracion_bp.route('/addpersonal',methods=['POST'])
@login_required
@check_permissions('ADMINISTRADOR')
def addpersonal():
	obj_consulta=MConfiguraciones(bd_current)
	Dni=request.form.get('Dni')
	nombre=request.form.get('NOMBRES')
	apellidopaterno=request.form.get('APELLIDOPATERNO')
	apellidomaterno=request.form.get('APELLIDOMATERNO')
	email=request.form.get('EMAIL')	

	params=(Dni,nombre,apellidopaterno,apellidomaterno,email)

	sql=f"INSERT INTO PERSONA(Dni,NOMBRES,APELLIDOPATERNO,APELLIDOMATERNO,EMAIL) VALUES(?,?,?,?,?)"
	nro=obj_consulta.Insertar(sql,params)
	return jsonify({'nro':nro})



@configuracion_bp.route('/listuser')
@login_required
@check_permissions('ADMINISTRADOR')
def listuser():
	obj_consulta=MConfiguraciones(bd_current)
	sql=f"""SELECT U.iduser,U.usua,U.DNI,P.NOMBRES,P.APELLIDOPATERNO,P.APELLIDOMATERNO,R.Nombre
			FROM Usuario AS U INNER JOIN PERSONA AS P ON U.DNI=P.Dni INNER JOIN usuarios_roles AS RU ON 
			RU.id_usuario=U.iduser INNER JOIN ROL AS R ON RU.id_rol=R.Id_Rol"""
	rows=obj_consulta.consultaUsuariosCompleto(sql)
	data=[{'iduser':val.iduser,'usuario':val.usua,'DNI':val.DNI,'NOMNBRES':val.NOMBRES,'APELLIDOPATERNO':val.APELLIDOPATERNO,
	'APELLIDOMATERNO':val.APELLIDOMATERNO,'ROL':val.Nombre} for val in rows]
	
	html=render_template('config/usuario.html')

	return jsonify({'html':html,'data':data})
	
@configuracion_bp.route('/adduser',methods=['POST'])
@login_required
@check_permissions('ADMINISTRADOR')
def AddUser():
	obj_consulta=MConfiguraciones(bd_current)
	sql=f"SELECT * FROM USUARIO WHERE DNI=?"
	dni=request.form.get('dni')
	rows=obj_consulta.cosultarDatosParams(sql,(dni,))
	if not rows:
		sql1=f"SELECT * FROM USUARIO WHERE usua=?"
		usua=request.form.get('usuario')
		rows_user=obj_consulta.cosultarDatosParams(sql1,(usua,))
		if not rows_user:
			contrasena=request.form.get('contrasena')
			rol=request.form.get('rol')
			print(dni,usua,contrasena,rol)
			return [1]
		else:
			return [2]
	else:
		return [3]


@configuracion_bp.route('/filllistrol',methods=['POST'])
@login_required
@check_permissions('ADMINISTRADOR')
def listrol():
	obj_consulta=MConfiguraciones(bd_current)
	sql=f"""SELECT * FROM ROL"""
	rows=obj_consulta.consultaUsuariosCompleto(sql)
	data=[{'Id_Rol':val.Id_Rol,'namerol':val.Nombre} for val in rows]
	
	html=render_template('config/usuario.html')

	return jsonify({'html':html,'data':data})
