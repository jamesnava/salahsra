from flask import Blueprint,render_template,redirect,url_for,request,g,abort
from flask_login import login_required,current_user
from functools import wraps
from app.models import querySala


main_bp=Blueprint('main',__name__,url_prefix='/main')


def check_permissions(required_role):
	def decorator(f):		
		@wraps(f)
		def decorated_function(*args,**kwargs):
						
			obj_sala=querySala()			
			rows=obj_sala.ConsultaRoles(current_user.id)
			lista_roles=[val.Nombre for val in rows]			
			if not required_role==lista_roles:
				abort(403)
			return f(*args,**kwargs)
		return decorated_function
	return decorator
	
@main_bp.app_context_processor
def inject_user_roles():
	if current_user.is_authenticated:
		obj_sala=querySala()
		rows_roles=obj_sala.ConsultaRoles(current_user.id)
		lista_roles=[val.nombrepermiso for val in rows_roles]
		return {'user_roles':lista_roles}
	return {'user_roles':[]}


@main_bp.route('/principal')
@login_required
#@check_permissions('ADMINISTRADOR')
def principal():
	obj_sala=querySala()
	user=obj_sala.Cargarusuario('iduser',current_user.id)	
	return render_template('base.html',usuario=user.username)