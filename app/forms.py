from flask_wtf import FlaskForm
from wtforms import StringField,TimeField,DecimalField,SelectField,DateField
from wtforms import TextAreaField,PasswordField,BooleanField,SubmitField,IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	usuario=StringField('Usuario',validators=[DataRequired()])
	clave=PasswordField('Clave',validators=[DataRequired()])
	recordar=BooleanField('Recordar')
	btn_iniciar=SubmitField('Iniciar')

class SalaForm(FlaskForm):
	HC=IntegerField('HC:',validators=[DataRequired()])
	datos=StringField('Datos Personales',validators=[DataRequired()])
	Tipo_Intervecion=SelectField('Tipo Quirurgia')
	UPPS=SelectField('UPPS')
	COMPLEJIDAD=SelectField('Complejidad')
	DX1=StringField('Diagnostico I',validators=[DataRequired()])
	DX2=StringField('Diagnostico II')
	IntervencionQ=StringField('Intervencion Quirurgica')
	DX1POST=StringField('Diagnostico Pos I')
	DX2POST=StringField('Diagnostico Pos II')
	ReIntervecion=SelectField('ReIntervecion')
	Cirujano=StringField('Cirujano')
	Anestesiologo=StringField('Anestesiologo')
	InstrumentalistaI=StringField('Instrumentalista I')
	InstrumentalistaII=StringField('Instrumentalista II')
	FechaIngreso=DateField('Fecha Ingreso',validators=[DataRequired()])
	HoraIngreso=TimeField('Hora Ingreso',validators=[DataRequired()])
	FechaSalida=DateField('Fecha Salida',validators=[DataRequired()])
	HoraSalida=TimeField('Hora Salida',validators=[DataRequired()])
	TiempoUso=StringField('Uso')
	Derivado=StringField('Derivar a',validators=[DataRequired()])
	Financiamiento=SelectField('Financiamiento')
	Observacion=TextAreaField('Observacion')
	Responsable=StringField('Responsable')
	Situacion=SelectField('Situacion')
	guardar=SubmitField('Guardar')


