import pyodbc
from app.codificacion import descifrar,cifrar

class Conexion_Galen(object):
	def __init__(self):		
		self.llave='qBBws2UNvFJNFZ5oRh5yx04AIhSzhCgjsfS3Q44QL_M='
	def ejecutar_conn(self):
		servidor='192.168.1.4'
		bd='SIGH'
		USER='Z0FBQUFBQm5CWGE3dEJ0SGdjOXgycFNyTEZ1ZFdwbUZQNWVrYTBFN0tRUjV6Y2NUZll6YXVSbkNjUU1IS0kwX2ZnTE9MSVpEcjFZc2lKamVQQjVoSENtR29nWE9UM0RqcVE9PQ=='
		PASSWORD='Z0FBQUFBQm5CVzFmUGR4eFNGX3Vfb0JFdXZ6RGNkWnNFQklWZTVaSkZHUjduS2pScFpqYUN4amxQd3QwVUYxLVVyYkZ3X2xDSEVRR0NOUzBHVEVUaTlkRlNaVzdHSUt6U2c9PQ=='
		
		user1=descifrar(self.llave,USER)
		pwd=descifrar(self.llave,PASSWORD)
		driver='{SQL Server}'					
		self.conn = pyodbc.connect(f"""DRIVER={driver};SERVER={servidor};DATABASE={bd};UID={user1};PWD={pwd}""")		
	def get_cursor(self):
		try:
			self.puntero=self.conn.cursor()
			return self.puntero
		except Exception as e:
			print('No pudo conectarse al servidor SISGALENPLUS')		
		
	def close_conection(self):
		self.conn.close()

class Conexion_Triaje(object):
	def __init__(self):		
		self.llave='qBBws2UNvFJNFZ5oRh5yx04AIhSzhCgjsfS3Q44QL_M='
	def ejecutar_conn(self):
		servidor='192.168.1.3'
		bd='SALA'
		USER='Z0FBQUFBQm5CWHdoR0xHdzVxV01qOF9kRS1kZEczZng0X21OZ1lHeUJkVGlJbFl6a19fY0czaUVBVWlPbl9ERktJd3pCUHZ2aTNjSXcwNHFIaXhqaTFodEdlNUFFQlZHSHc9PQ=='
		PASSWORD='Z0FBQUFBQm5CWDA2Sjk0QkJSNTFPcEdrNGhIWEtSRGJMU3RNOHNwRGl3b0prbGdfSl83YzBnQmYwbWhGWXZwNGZqN0dtWUNKR1VXMk5aWXJvQUpsQXJQWWVWSzNJaUhibFE9PQ=='

		user1=descifrar(self.llave,USER)
		pwd=descifrar(self.llave,PASSWORD)
		driver='{SQL Server}'					
		self.conn = pyodbc.connect(f"""DRIVER={driver};SERVER={servidor};DATABASE={bd};UID={user1};PWD={pwd}""")		
	def get_cursor(self):
		try:
			self.puntero=self.conn.cursor()
			return self.puntero
		except Exception as e:
			print('No pudo conectarse al servidor SISGALENPLUS')		
		
	def close_conection(self):		
		self.conn.close()


	
