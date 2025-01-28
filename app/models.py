from app.conect_bd import Conexion_Galen,Conexion_Triaje,Conexion_TriajeHIS
from werkzeug.security import generate_password_hash,check_password_hash
from app.usermodel import User
#from app import login
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
	def consultarDatosPaciente(self,HC):
		obj_conectar=Conexion_Galen()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		rows=[]
		try:
			
			sql=f"""SELECT P.NroDocumento,P.PrimerNombre,P.ApellidoPaterno,P.ApellidoMaterno,DIS.Nombre AS DISTRITO,PRO.Nombre AS PROVINCIA,DEPA.Nombre AS DEPARTAMENTO 
			FROM Pacientes AS P LEFT JOIN Distritos AS DIS ON P.IdDistritoProcedencia=DIS.IdDistrito
			LEFT JOIN Provincias AS PRO ON DIS.IdProvincia=PRO.IdProvincia LEFT JOIN Departamentos AS DEPA ON 
			PRO.IdDepartamento=DEPA.IdDepartamento WHERE P.NroHistoriaClinica='{HC}'
			"""			
			cursor.execute(sql)
			rows=cursor.fetchall()
			

		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows



class querySala:
	def __init__(self):
		self.password_hash=None
	def set_password(self,password):
		self.password_hash=generate_password_hash(password)
	def check_password(self,password0,password1):
		return check_password_hash(password0,password1)

	
	def Cargarusuario(self,campo,user_id):

		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		rows=None
		try:
			sql=f"""SELECT iduser, usua, clave FROM Usuario WHERE {campo} = ?"""
			
			cursor.execute(sql,(user_id,))
			rows=cursor.fetchone()
			
		except Exception as e:
			raise e
		finally:
			if rows:

				return User(rows[0],rows[1],rows[2])
			else:
				return None


	def ConsultaRoles(self,user_id):

		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		rows=None
		try:
			sql=f"""SELECT R.Nombre,PER.nombrepermiso FROM USUARIO AS U INNER JOIN usuarios_roles AS UR ON 
				U.iduser=UR.id_usuario INNER JOIN ROL AS R ON UR.id_rol=R.Id_Rol INNER JOIN 
				permiso_roles AS PR ON R.Id_Rol=PR.Id_Rol INNER JOIN Permiso AS PER ON PR.Id_Per=PER.Id_Per WHERE U.iduser=?"""
			
			cursor.execute(sql,(user_id,))
			rows=cursor.fetchall()
			
		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()			
			return rows
			

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

	def consultarTablaDate(self,tabla,campo,fechai,fechas):
		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""SELECT * FROM {tabla} WHERE {campo} BETWEEN ? AND ?"""			
			cursor.execute(sql,(fechai,fechas))
			rows=cursor.fetchall()

		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows


	def consultarTablaCantidad(self,tabla,cantidad,fecha):
		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""SELECT TOP {cantidad} * FROM {tabla} ORDER BY {fecha} DESC"""	
				
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
			
			sql=f"""select top 50 S.Id_Sala,S.HC,S.Fech_Ingre,U.Id_URPA from Sala as S 
			LEFT JOIN URPA AS U ON S.Id_Sala=U.Id_Sala WhEre U.Id_URPA is null order by Id_Sala desc"""					
			cursor.execute(sql)
			rows=cursor.fetchall()

		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def consultarUrpa(self):
		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""select top 50 S.Id_Sala,S.HC,S.Fech_Ingre,U.Id_URPA from Sala as S 
			right JOIN URPA AS U ON S.Id_Sala=U.Id_Sala ORder bY Id_URPA Desc"""					
			cursor.execute(sql)
			rows=cursor.fetchall()

		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows
				
	def consultarIdTable(self,tabla,campo):
		obj_conectar=Conexion_Triaje()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""select top 1 {campo} AS idtabla from {tabla} OrDer by {campo} dESC"""					
			cursor.execute(sql)
			rows=cursor.fetchall()

		except Exception as e:
			raise e
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows


class queryHIS:
	def __init__(self):
		pass
	def consultarAtenciones(self):
		rows=[]
		columnas=[]
		obj_conectar=Conexion_TriajeHIS()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""SELECT T.Fecha_Atencion,MP.Numero_Documento,MP.Nombres_Personal+' '+MP.Apellido_Paterno_Personal+' '+MP.Apellido_Materno_Personal AS DatosP,
					T.Id_Ups, COUNT(*) AS cantidad FROM TRAMA AS T INNER JOIN MAESTRO_PERSONAL AS MP ON T.Id_Personal=MP.Id_Personal
					WHERE Fecha_Atencion BETWEEN '2016-01-01' AND '2016-12-31' GROUP BY T.Fecha_Atencion,MP.Numero_Documento,MP.Nombres_Personal+' '+
					MP.Apellido_Paterno_Personal+' '+MP.Apellido_Materno_Personal,T.Id_Ups"""					
			cursor.execute(sql)
			rows=cursor.fetchall()
			columnas=[columns[0] for columns in cursor.description] 

		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return columnas,rows
	def consultarAtencionCampos(self,idcita,codigo_item,fecha,lote):
		rows=[]		
		obj_conectar=Conexion_TriajeHIS()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""SELECT * FROM TRAMA WHERE Id_Cita=? AND Codigo_Item=? 
			AND Fecha_Atencion=? AND Lote=?"""					
			cursor.execute(sql,(idcita,codigo_item,fecha,lote))
			rows=cursor.fetchall()
			

		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def consultarAtencionParametro(self,tabla,campo,valor):
		rows=[]		
		obj_conectar=Conexion_TriajeHIS()
		obj_conectar.ejecutar_conn()
		cursor=obj_conectar.get_cursor()
		try:
			
			sql=f"""SELECT * FROM {tabla} WHERE {campo}='{valor}'"""					
			cursor.execute(sql)			
			rows=cursor.fetchall()		

		except Exception as e:
			print(e)
		finally:
			cursor.close()
			obj_conectar.close_conection()
			return rows

	def InsertTable(self,tabla,diccionario):
		obj_conectar=Conexion_TriajeHIS()
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
			return diccionario
		finally:
			cursor.close()
			obj_conectar.close_conection()

			
		


