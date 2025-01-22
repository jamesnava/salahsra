from flask import Blueprint,render_template,redirect,url_for,request
from flask_login import login_required


main_bp=Blueprint('main',__name__,url_prefix='/main')

@main_bp.route('/principal')
@login_required
def principal():
	return render_template('base.html')