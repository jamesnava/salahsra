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

def tolist(tabla,cantidad,fecha):
	from app.models import queryGalen,querySala
	obj_modelo=querySala()
	obj_galen=queryGalen()
	rowsRegistros=obj_modelo.consultarTablaCantidad(tabla,cantidad,fecha)

	lista=[]
	for val in rowsRegistros:
		HC=val.HC
		rowsGalen=obj_galen.consultarTabla('Pacientes','NroHistoriaClinica',HC)
		datos=rowsGalen[0].PrimerNombre+' '+rowsGalen[0].ApellidoPaterno+' '+rowsGalen[0].ApellidoMaterno if rowsGalen else '' 
		if fecha=='Fech_Ingre':		
			lista.append([val.Id_Sala,datos,HC,val.Inter_Q,val.UPPS,val.COMPLEJIDAD,val.Fech_Ingre])
		else:
			rowsMotivo=obj_modelo.consultarTablaCondition('MOTIVOSUSPENCION','idmotivo',val.idmotivo)
			lista.append([val.idsuspendidas,datos,rowsMotivo[0].descripcion,val.fechasuspencion,val.HC])
	return lista
def validarcampos(diccionario):
	valor=''
	for key,val in diccionario.items():
		if len(val)<1:
			valor=key
			break
		valor=1
	return valor

