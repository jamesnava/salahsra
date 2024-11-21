def todictionario(rows,*args):
	diccionario={}
	for val in rows:
		for clave in args:
			diccionario[clave]=getattr(val,clave)
	return diccionario

		
def toSelect(rows,index,valor):
	opciones=[]
	for val in rows:
		opciones.append((getattr(val,index),getattr(val,valor)))

	return opciones

def tolist(tabla,cantidad):
	from app.models import queryGalen,querySala
	obj_modelo=querySala()
	obj_galen=queryGalen()
	rowsRegistros=obj_modelo.consultarTablaCantidad(tabla,cantidad)

	lista=[]
	for val in rowsRegistros:
		HC=val.HC
		rowsGalen=obj_galen.consultarTabla('Pacientes','NroHistoriaClinica',HC)
		datos=rowsGalen[0].PrimerNombre+' '+rowsGalen[0].ApellidoPaterno+' '+rowsGalen[0].ApellidoMaterno if rowsGalen else '' 
		
		lista.append([val.Id_Sala,datos,HC,val.Inter_Q,val.UPPS,val.COMPLEJIDAD,val.Fech_Ingre])
	return lista
