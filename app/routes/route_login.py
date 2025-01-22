from flask import Blueprint, render_template,redirect,url_for,request
from flask_login import login_user,login_required,current_user,logout_user
from app.forms import LoginForm
from app.models import queryGalen,querySala


auth_bp=Blueprint('auth',__name__,url_prefix='/auth')


@auth_bp.route('/logout')
def salir():
	logout_user()
	return redirect(url_for('auth.inicio'))

@auth_bp.route('/',methods=['POST','GET'])
def inicio():
	form=LoginForm()
	obj_consulta=querySala()
	if request.method=='POST':
		username=form.usuario.data
		password=form.clave.data
		recordar=form.recordar.data
		user=obj_consulta.Cargarusuario('usua',username)

		if user and user.password==password:
			login_user(user,remember=recordar)
			next_page = request.args.get('next')
			
			return redirect(next_page or url_for('main.principal'))
	
	return render_template('inicio.html',form=form)