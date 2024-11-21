var idSalaEditar;

function Llenardatos(event){
	if (event){
		event.preventDefault();
	}
	var hc=$('#CampoHC').val()

	$.ajax({
		url:'/llenardatospaciente',
		type:'POST',
		data:{
			hc:hc
		},
		success:function(response){
			
			$('#NombresApellidos').val(response.PrimerNombre+' '+response.ApellidoPaterno+' '+response.ApellidoMaterno);
		},
		error:function(){
			console.error('Error al enviar solicitud')
		}
	});
}


function BuscarInstrumentista(campo,tabla,iddiv,bd){
	
	var val=$('#'+campo).val()
	if (val.length>1){
	$.ajax({
		url:'/search',
		type:'POST',
		data:{
			val:val,
			tabla:tabla,
			bd:bd
		},
		success:function(response){
			var resultadosHtml='';
			$.each(response,function(index,valor){
				resultadosHtml+='<p style="cursor: pointer;background:#666a70" onclick="SeleccionarInstrumentalista(\'' + valor + '\',\''+iddiv+'\',\''+campo+'\')">' + valor + '</p>';
			});
			$('#'+iddiv).show()
			$('#'+iddiv).html(resultadosHtml);
		},
		error:function(){
			console.error('Error al enviar solicitud')
		}
		});
	}
	else{
		
		$('#'+iddiv).hide()
	}
}
 function SeleccionarInstrumentalista(valorSeleccionado,iddiv,campo) {
        $('#'+campo).val(valorSeleccionado); 
        $('#'+iddiv).hide();  
    }

function calculardiferencia(fechai,horai,fechas,horas,uso){
	var fechaingreso=$('#'+fechai).val()
	var horaingreso=$('#'+horai).val()
	var fechasalida=$('#'+fechas).val()
	var horasalida=$('#'+horas).val()
		if (fechaingreso!=='' && horaingreso!=='' && fechasalida!==''){
		fechainicio=new Date(`${fechaingreso}T${horaingreso}:00`);
		fechafin=new Date(`${fechasalida}T${horasalida}:00`);
		
		const diferencia=fechafin-fechainicio;		
		const diferenciahoras=diferencia/(1000*60*60)
		$('#'+uso).val(diferenciahoras)
	}
	else{
		alert('llene los campos de la fecha y hora, para generar el calculo')
	}

}

function abrirModal(idmodal,formulario) { 
	$('#'+formulario)[0].reset();    
    $('#'+idmodal).modal('show');
    }

function LimpiarCampo(idcampo){

	$('#'+idcampo).val('')
	}

function abrirModalAciones(idmodal,formulario,id) { 	 
    $('#'+idmodal).modal('show');
    idSalaEditar=id;
    }

function LlenarSelect(sourcecampo,tabla,selectdestino,bd,condicion){
	var origen=$('#'+sourcecampo).val()	
	
	$.ajax({
		url:'/fillselect',
		type:'POST',
		data:{
			tabla:tabla,
			condicionvalor:origen,
			condicion:condicion,
			bd:bd
		},
		success:function(response){
			var resultadosHtml='';
			$.each(response,function(index,valor){
				resultadosHtml+='<p style="cursor: pointer;background:#666a70" onclick="SeleccionarInstrumentalista(\'' + valor + '\',\''+iddiv+'\',\''+campo+'\')">' + valor + '</p>';
			});
			
		},
		error:function(){
			console.error('Error al enviar solicitud')
		}
		});
	
}

function versala(idmodal,formulario,cod){		
		let codigo=cod;
		$('#'+idmodal).modal('show');
		$.ajax({
			url:'/versala',
			type:'POST',
			data:{
				codigo:codigo
			},
			success:function(response){
				$('#divversala').empty();
				$('#divversala').html($('#divversala').html()+`<p><strong>Historia :</strong> ${response[0].HC}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Tipo Interv Q :</strong> ${response[0].Inter_Q}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>UPPS :</strong> ${response[0].UPPS}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Complejidad :</strong> ${response[0].COMPLEJIDAD}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Primer DX :</strong> ${response[0].DX1}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Segundo DX :</strong> ${response[0].DX2}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Procedimiento :</strong> ${response[0].INTQ}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Primer DX POST:</strong> ${response[0].DX1POST}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Primer DX POST :</strong> ${response[0].DX2POST}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Cirujano :</strong> ${response[0].CIRUJANO}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Anestesiologo :</strong> ${response[0].ANESTESIOLOGO}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>1er Instrumentista :</strong> ${response[0].INSTRUMENTISTAI}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>2do Instrumentista :</strong> ${response[0].INSTRUMENTISTAII}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Fecha Ingreso :</strong> ${response[0].FECHAINGRESO}</p>`);
			}
		});
	
}

function eliminarSala(cod){
	      let valor=cod;
		$.ajax(
		{url:'/deletesala',type:'POST',data:{
			valor:valor,
		},success:function(response){
			if (response==1){
				alert("Se eliminó correctamente el registro "+valor);
				location.reload(true);
			}
			else{
				alert("Error!!");
			}
			
		},error: function(){
			alert("No pudo Eliminarse");
		}});
	
}


$(document).ready(function(){
	$('.btn-eliminar').click(function(e){
		e.preventDefault();
		let valor=$(this).data('id');
		$.ajax(
		{url:'/deletesala',type:'POST',data:{
			valor:valor,
		},success:function(response){
			if (response==1){
				alert("Se eliminó correctamente el registro "+valor);
				location.reload(true);
			}
			else{
				alert("Error!!");
			}
			
		},error: function(){
			alert("No pudo Eliminarse");
		}});
	});


	$('#btnActualizaSala').click(function(e){
		e.preventDefault();
		
		let tipointervencion=$('#MtipoInter').val();
		let upss=$('#MUPSS').val();
		let complejidad=$('#Mcomplejidad').val();

		$.ajax({
			url:'/modificarsala',
			type:'POST',
			data:{
				tipointer:tipointervencion,
				upss:upss,
				complejidad:complejidad,
				codigo:idSalaEditar
			}, success:function(response){
				alert(response);
			},
			error: function(){

			}
		});

	});

	$('.verData').click(function(e){
		e.preventDefault()
		let codigo=$(this).data('id');
		$('#modalVisualizar').modal('show');
		$.ajax({
			url:'/versala',
			type:'POST',
			data:{
				codigo:codigo
			},
			success:function(response){
				$('#divversala').empty();
				$('#divversala').html($('#divversala').html()+`<p><strong>Historia :</strong> ${response[0].HC}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Tipo Interv Q :</strong> ${response[0].Inter_Q}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>UPPS :</strong> ${response[0].UPPS}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Complejidad :</strong> ${response[0].COMPLEJIDAD}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Primer DX :</strong> ${response[0].DX1}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Segundo DX :</strong> ${response[0].DX2}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Procedimiento :</strong> ${response[0].INTQ}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Primer DX POST:</strong> ${response[0].DX1POST}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Primer DX POST :</strong> ${response[0].DX2POST}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Cirujano :</strong> ${response[0].CIRUJANO}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Anestesiologo :</strong> ${response[0].ANESTESIOLOGO}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>1er Instrumentista :</strong> ${response[0].INSTRUMENTISTAI}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>2do Instrumentista :</strong> ${response[0].INSTRUMENTISTAII}</p>`);
				$('#divversala').html($('#divversala').html()+`<p><strong>Fecha Ingreso :</strong> ${response[0].FECHAINGRESO}</p>`);
			}
		})
	});


	$('#idsearch').keyup(function(e){
		e.preventDefault()
		let valor=$('#idsearch').val()
		
		$.ajax({
			url:'/search',
			type:'POST',
			data:{
				val:valor,
				tabla:'Sala',
				bd:'SALABUSQUEDA',
				},
			success:function(response){
				const tbody = $("#tabledata tbody");
				tbody.empty();
				$.each(response,function(index,valor){
					const tr=`<tr>
				<td>${valor[1]}</td>
				<td>${valor[2]}</td>
				<td>${valor[3]}</td>
				<td>${valor[4]}</td>
				<td>${valor[5]}</td>
				<td>${valor[6]}</td>
				<td><a href="#" onclick="abrirModalAciones('modalEditar','eformulario',${valor[0]})">Editar</a></td>
				<td><a href="#" onclick="versala('modalVisualizar','eformulario',${valor[0]})">Ver</a></td>
				<td><a href="#" onclick="eliminarSala(${valor[0]})" class="btn-eliminar">Eliminar</a></td>
				</tr>`
				tbody.append(tr);
				});
				
			}
		});
	});

});