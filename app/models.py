from app.conect_bd import Conexion_Galen,Conexion_Triaje
import traceback

class queryGalen:
	def __init__(self):
		pass
	def consultarTabla(self,tabla,condicion,valorcondicion):
		obj_conectar=Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""SELECT * FROM {tabla} WHERE {condicion}=?"""
			valor=valorcondicion
			cursor.execute(sql,(valor,))
			rows=cursor.fetchall()

		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
	def consultarTablaLike(self,tabla,condicion,condicion2,valorcondicion):
		obj_conectar=Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""SELECT * FROM {tabla} WHERE {condicion} COLLATE Latin1_General_CI_AI LIKE ? OR {condicion2} COLLATE Latin1_General_CI_AI LIKE ?"""
			valor=valorcondicion
			cursor.execute(sql,('%' + valor + '%','%'+valor+'%'))
			rows=cursor.fetchall()

		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
class querySala:
	def __init__(self):
		pass
	def consultarTabla(self,tabla):
		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""SELECT * FROM {tabla}"""			
			cursor.execute(sql)
			rows=cursor.fetchall()

		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def consultarTablaCantidad(self,tabla,cantidad):
		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""SELECT TOP {cantidad} * FROM {tabla} ORDER BY Fech_Ingre DESC"""			
			cursor.execute(sql)
			rows=cursor.fetchall()

		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def consultarCIELike(self,tabla,condicion,condicion2,valorcondicion):
		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""SELECT * FROM {tabla} WHERE {condicion} COLLATE Latin1_General_CI_AI LIKE ? OR {condicion2} LIKE ? """
			valor=valorcondicion
			cursor.execute(sql,('%' + valor + '%','%' + valor + '%'))
			rows=cursor.fetchall()

		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def consultarLike(self,tabla,condicion,valorcondicion,n):
		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			if n:
				sql=f"""SELECT * FROM {tabla} WHERE {condicion} COLLATE Latin1_General_CI_AI LIKE ? """
			else:
				sql=f"""SELECT * FROM {tabla} WHERE {condicion} COLLATE Latin1_General_CI_AI NOT LIKE ? """
			valor=valorcondicion			
			cursor.execute(sql,(valor + '%',))
			rows=cursor.fetchall()

		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def InsertTable(self,tabla,diccionario):
		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()

		try:
			
			columnas=[]
			valores=[]
			for clave,valor in diccionario.items():
				columnas.append(clave)
				valores.append(valor)
			
			col=f"({', '.join(columnas)})"
			
			sql=f"INSERT INTO {tabla} {col} VALUES {tuple(valores)}"
			
			cursor.execute(sql)
			cursor.commit()
			return cursor.rowcount
		except Exception as e:
			
			print(traceback.format_exc())
		finally:
			cursor.close()
			obj_conectar.close_conection()

	def deleteSala(self,ideliminar):
		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""DELETE Sala WHERE Id_Sala=?"""			
			valor=ideliminar
			
			cursor.execute(sql,(valor,))
			cursor.commit()
			estado=cursor.rowcount
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return estado

	def ModificarTabla(self,tabla,condicion,condicionvalor,data):
		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			sql=f"UPDATE {tabla} SET "
			sql1=""
			valores=[]
			for clave,valor in data.items():
				sql1=sql1+f"{clave}=?, "
				valores.append(valor)

			valores.append(condicionvalor)
			sql=sql+sql1[:-2]+f" WHERE {condicion}=?"				
			valores=tuple(valores)			
			cursor.execute(sql,valores)
			cursor.commit()
			estado=cursor.rowcount
		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return estado

	def consultarTablaCondition(self,tabla,condicion,valorcondicion):
		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""SELECT * FROM {tabla} WHERE {condicion}=? """
			
			valor=valorcondicion			
			cursor.execute(sql,(valor,))
			rows=cursor.fetchall()

		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def consultarLlenarUrpa(self):
		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""select top 50 S.HC,S.Fech_Ingre from Sala as S LEFT JOIN URPA AS U ON S.Id_Sala=U.Id_Sala ORDER BY S.Fech_Ingre DESC"""					
			cursor.execute(sql)
			rows=cursor.fetchall()

		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows


			
		



