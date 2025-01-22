var idSalaEditar;
//menue

$(document).ready(function() {
    $('.category-link').click(function(e) {
        e.preventDefault();        
        $(this).next('.sub-menu').slideToggle();
    });
});


function Llenardatos(event,campo,valor){

	if (event){
		event.preventDefault();
	}
	var hc=$('#'+campo).val()	
	$.ajax({
		url:'/salabp/llenardatospaciente',
		type:'POST',
		data:{
			hc:hc
		},
		success:function(response){
			
			$('#'+valor).val(response.PrimerNombre+' '+response.ApellidoPaterno+' '+response.ApellidoMaterno);
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
		url:'/salabp/search',
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
		const diferenciasegundos=Math.floor(diferencia/1000);
		//calcular horas, minutos y segundos
		const horas=Math.floor(diferenciasegundos/3600);
		const minutos=Math.floor((diferenciasegundos%3600)/60);
		const segundos=diferenciasegundos%60;

		const formatoTiempo = String(horas).padStart(2, '0') + ':' + String(minutos).padStart(2, '0') + ':' +String(segundos).padStart(2, '0');

		$('#'+uso).val(formatoTiempo)
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
	$('#'+formulario)[0].reset();   	 
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
			url:'/salabp/versala',
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
		{url:'/salabp/deletesala',type:'POST',data:{
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
		{url:'/salabp/deletesala',type:'POST',data:{
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
			url:'/salabp/modificarsala',
			type:'POST',
			data:{
				tipointer:tipointervencion,
				upss:upss,
				complejidad:complejidad,
				codigo:idSalaEditar
			}, success:function(response){
				if (response==1){
					alert("Se modificó correctamente!!")
					location.reload(true);
				}
				
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
			url:'/salabp/versala',
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
			url:'/salabp/search',
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

	


  $('#modalInsertUrpa').on('shown.bs.modal', function () {
    const selectElement = $('#selectAnestesia');
    selectElement.empty();
    $.ajax({
    	url:'/salabp/llenarAnestesia',
    	type:'POST',
    	data:'ninguno',
    	success: function(response){
    		response.forEach(opcion => {
       		 selectElement.append(`<option value="${opcion.value}">${opcion.text}</option>`);
      		});
    		
    	}
    });
});


$('#btnguardarurpa').on('click',function(){
	let tiempoespera=$('#tiempoespera').val()
	let Fechaingreso=$('#FechaIurpa').val()
	let Horaingreso=$('#HoraIurpa').val()
	let FehaSalida=$('#FechaSurpa').val()
	let HoraSalida=$('#HoraSurpa').val()
	let permanencia=$('#Permanencia').val()
	let derivar=$('#idderrivarurpa').val()
	let responsable=$('#iddivurpainstrumentista').val()
	let tipoanestecia=$('#selectAnestesia').val()
	params={'Id_Sala':idSalaEditar,'tiempoespera':tiempoespera,'Fechaingreso':Fechaingreso,'Horaingreso':Horaingreso,
	'FehaSalida':FehaSalida,'HoraSalida':HoraSalida,'permanencia':permanencia,'derivar':derivar,'responsable':responsable,
	'tipoanestecia':tipoanestecia}

	$.ajax({
		url:'/salabp/inserturpa',
		type:'POST',
		data:params,
		success:function(response){
			if (response==1){
				alert("se insertó correctamente!!")
				$('#modalInsertUrpa').hide(); 
				location.reload(true);
			}
			else{
				alert('debe llenar el campo '+response)
			}
		}
	});

});




$('#btnradio1').on('click',function(){
	$('#mprogramado').modal('show');

	const selectElemento=$('#selectmotivo');
	selectElemento.empty();
	$.ajax({
		url:'/salabp/programado',
		type:'POST',
		success:function(response){
			response.forEach(opcion=>{
				selectElemento.append(`<option value="${opcion.value}">${opcion.text}</option>`)
			});

	}});
});



//guardar cirugias programadas

$('#btnCirugiasSuspendidas').on('click',function(){
	var HC=$('#CampoHCSUS').val();
	var Id_Cie=$('#DXSUS').val();
	var Id_Motivo=$('#selectmotivo').val();
	var descmotivo=$('#descmotivo').val();
	var responsable=$('#respoSUS').val();
	var solucion=$('#propuestasolucion').val();
	var Fechasus=$('#fechasuspencion').val();
	params={'Id_Cie':Id_Cie,'idmotivo':Id_Motivo,'descripcionmotivo':descmotivo,
	'solucionp':solucion,'responsable':responsable,'fechasuspencion':Fechasus,'HC':HC}
	$.ajax({url:'/salabp/insertsus',
		type:'POST',
		data:params,
		success:function(response){
			if (response==1){
				alert('Se insertó correctamente!')
				$('#mprogramado').hide();
				location.reload(true);

			}
			else{
				alert('debe llenar el campo '+response)
			}

	}});
});

var valoroculto;

$('#rsala,#rurpa').click(function(event){
	var elementoorigen=$(event.target);
	var idelemento=elementoorigen.attr('id');	
	$('#ReporteSala').modal('show');
	valoroculto=idelemento;
});

$('#generarReporteSala').click(function(){
		var fechai = $('#dateSafter').val();
        var fechas = $('#dateSbefore').val();
        
        if (!fechai || !fechas) {
            alert("Por favor, selecciona las fechas.");
            return;
        }

        // Asignar valores al formulario
        $('#inputFechaI').val(fechai);
        $('#inputFechaS').val(fechas);
        $('#categoria').val(valoroculto);
        // Enviar el formulario para descargar el archivo
        $('#formGenerarReporte').submit();

        // Detectar finalización de la descarga cerrando el modal después de un tiempo
        setTimeout(function() {
        var modal = bootstrap.Modal.getInstance(document.getElementById('ReporteSala'));
        modal.hide(); }, 1000);

	});
});

