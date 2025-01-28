from flask import Blueprint,render_template,request,g,abort,flash, redirect,url_for,jsonify
from flask_login import login_required,current_user
from functools import wraps
from app.models import querySala
from app.modelos.modconfiguraciones.queryconfiguracion import MConfiguraciones 


configuracion_bp=Blueprint('cfg',__name__,url_prefix='/cfg')

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
	obj_consulta=MConfiguraciones('salap')
	rows=obj_consulta.consultaPersonales()
	data=[{'Dni':val.Dni,'NOMBRES':val.NOMBRES,'APELLIDOS':val.APELLIDOPATERNO+' '+val.APELLIDOMATERNO} for val in rows]
	html=render_template('config/personal.html')

	return jsonify({'html':html,'data':data})