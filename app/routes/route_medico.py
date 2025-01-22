from flask import Blueprint,render_template
from flask_login import login_required

medico_bp=Blueprint('medico',__name__,url_prefix='/medico')

@medico_bp.route('/estadisticamedico')
@login_required
def estadisticomedico():
	return render_template('estadisticamedico.html')

@medico_bp.route('/configuracion')
@login_required
def confgmedico():
	return render_template('configuracionmedico.html')