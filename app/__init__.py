from flask import Flask
from config import Config
from flask_login import LoginManager
from dash import Dash
from app.models import querySala
from app.routes.route_login import auth_bp
from app.routes.route_principal import main_bp
from app.routes.route_medico import medico_bp
from app.routes.route_sala import sala_bp
from app.routes.route_configuracion import configuracion_bp

app=Flask(__name__)
app.config.from_object(Config)
login=LoginManager()
login.init_app(app)
login.login_view='auth.inicio'

@login.user_loader
def load_user(id_user):
	obj_consulta=querySala()	 
	user=obj_consulta.Cargarusuario('iduser',id_user)	
	return user


from app.graficos.medico.dashmedico import init_dash_app

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(medico_bp)
app.register_blueprint(sala_bp)
app.register_blueprint(configuracion_bp)
dash_app=init_dash_app(app)

#from app import routes