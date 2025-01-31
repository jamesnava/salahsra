from app.conect_bd import Conexion_BD
class MConfiguraciones:
	def __init__(self,bd):
		self.bd=bd
	def consultaPersonales(self,query):
		try:
			with Conexion_BD(self.bd) as con:
				cursor=con.cursor()
				cursor.execute(query)
				return cursor.fetchall()

		except Exception as e:
			print(e)
		
	def consultaUsuariosCompleto(self,query):
		try:
			with Conexion_BD(self.bd) as con:
				cursor=con.cursor()
				cursor.execute(query)
				return cursor.fetchall()

		except Exception as e:
			print(e)
			
	def cosultarDatosParams(self,query,params):
		try:
			with Conexion_BD(self.bd) as conn:
				cursor=conn.cursor()
				cursor.execute(query,params)
				return cursor.fetchall()
		except Exception as e:
			raise e

	def Insertar(self,query,params):
		try:
			with Conexion_BD(self.bd) as con:
				cursor=con.cursor()
				cursor.execute(query,params)
				cursor.commit()
				return cursor.rowcount
		except Exception as e:
			print(e)
		