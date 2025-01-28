from flask import Blueprint,render_template,request,g,abort
from flask_login import login_required,current_user


configuracion_bp=Blueprint('cfg',__name__,url_prefix='/cfg')

@configuracion_bp.route('/config')
@login_required
def configuracion():
	return render_template('config/configuraciongeneral.html')

@login_required
@configuracion_bp.route('/userconfig')
def userconf():
	return render_template('config/usermenu.html')

@login_required
@configuracion_bp.route('/mostrarpersonal')
def mostrarpersonal():
	return render_template('config/personal.html')