from flask import Blueprint,render_template,request
from flask_login import login_required

configuracion_bp=Blueprint('cfg',__name__,url_prefix='/cfg')

@login_required
@configuracion_bp.route('/config')
def configuracion():
	return render_template('config/configuraciongeneral.html')
@login_required
@configuracion_bp.route('/userconfig')
def userconf():
	return render_template('config/usermenu.html')