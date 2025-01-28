from app.conect_bd import Conexion_BD
class MConfiguraciones:
	def __init__(self,bd):
		self.bd=bd
	def consultaPersonales(self):		
		with Conexion_BD(self.bd) as con:
			cursor=con.cursor()
			cursor.execute('SELECT * FROM PERSONA')
			return cursor.fetchall()
