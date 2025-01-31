$(document).ready(function(){

	$('#configuser').click(function(){
		$.ajax({
			url:'/cfg/userconfig',
			type:'GET',
			success: function(response){
				$('#user-submenu').html(response);
				
			}
		});
	});

	$('#user-submenu').on('click','#addpersona',function(){
		$.ajax({
			url:'/cfg/listarpersonal',
			type:'GET',
			success:function(response){
			 $('#contenedoracceso').html(response.html);
			 let TableBody=$('#tabla-personal tbody');
			 TableBody.empty();
			 response.data.forEach(function(row){
			 	let newRow=`<tr>
			 	<td>${row.Dni}</td>
			 	<td>${row.NOMBRES}</td>
			 	<td>${row.APELLIDOS}</td>
			 	<td><button class='btn btn-primary'>Editar</button></td>			 				 	
			 	</tr>`;
			 	TableBody.append(newRow);
			 });
			}
		});
	});

	$('#user-submenu').on('click','#btnInsertarPersonal',function(){
		$('#modalInsertPersonal').modal('show');
		
	});

	$('#user-submenu').on('click','#btnguardarpersonal',function(){

		let dni=$('#PDni').val();
		let nombre=$('#PNombre').val();
		let apellidopaterno=$('#PAPaterno').val();
		let apellidomaterno=$('#PAMaterno').val();
		let email=$('#PEmail').val();
		params={'Dni':dni,'NOMBRES':nombre,'APELLIDOPATERNO':apellidopaterno,'APELLIDOMATERNO':apellidomaterno,'EMAIL':email}
		$.ajax({
			url:'/cfg/addpersonal',
			type:'POST',
			data:params,
			success: function(response){
			if (response.nro==1){
				alert("Seccess");
				location.reload(true);
			}
			else{
				alert('No pudo insertarse')
				location.reload(true);
			}

			}
		});

		 });


	$('#user-submenu').on('click','#Ausuario',function(){
		$.ajax({
			url:'/cfg/listuser',
			type:'GET',
			success: function(response){
				$('#contenedoracceso').html(response.html)
				let TableBody=$('#tabla-usuario tbody');
				TableBody.empty();
				response.data.forEach(function(row){
					let NewRow=`<tr>
					<td>${row.NOMNBRES}</td>
					<td>${row.APELLIDOPATERNO} ${row.APELLIDOMATERNO}</td>
					<td>${row.usuario}</td>
					<td>${row.ROL}</td>
					<td><button class="btn btn-success" id="btnEditarUser">Editar</button></td>

					</tr>`;
				TableBody.append(NewRow);
				});
			}
		});



	});

$('#user-submenu').on('click','#btnAgregarUsuario',function(){
		$('#modalInsertUsuario').modal('show');
		$.ajax({
			url:'/cfg/filllistrol',
			type:'POST',
			success: function(response){
				let seleccionHtml=$('#USelectRol');
				seleccionHtml.empty();

				response.data.forEach(function(row){
					seleccionHtml.append(`<option value="${row.Id_Rol}">${row.namerol}</option>`);

				});
				seleccionHtml.trigger('change');
			}
		});		
	});

$('#user-submenu').on('click','#btnguardarusuario',function(){
	let dni=$('#UDni').val();
	let usuario=$('#Uusuario').val();
	let contrasena=$('#Ucontra').val();
	let rol=$('#UESelectRol').val();
	alert($('#UESelectRol option:selected').val());
	alert($('#UESelectRol option:selected').text());
	$.ajax({
		url:'/cfg/adduser',
		type:'POST',
		data:{'dni':dni,'usuario':usuario,'contrasena':contrasena,'rol':rol},
		success: function(response){			
			if (response==1)				
				{
				$('#modalInsertUsuario').modal('hide').data('bs.modal',null);				
				$('#cuerpomessage').append('<img src="/static/img/user/check.png">');	
				$('#cuerpomessage').append('<p>Se insertó correctamente!!</p>');				
				$('#miModal').modal('show');
				setTimeout(function(){location.reload(true);},3000);					
				
			}
			if (response==2){
				$('#modalInsertUsuario').modal('hide').data('bs.modal',null);				
				$('#cuerpomessage').append('<img src="/static/img/user/denied.png">');	
				$('#cuerpomessage').append('<p>Elige un usuario diferente !!</p>');				
				$('#miModal').modal('show');
				setTimeout(function(){location.reload(true);},3000);
			}
			if(response==3){
				$('#modalInsertUsuario').modal('hide').data('bs.modal',null);				
				$('#cuerpomessage').append('<img src="/static/img/user/denied.png">');	
				$('#cuerpomessage').append('<p>El personal ya cuenta con un usuario!!</p>');				
				$('#miModal').modal('show');
				setTimeout(function(){location.reload(true);},3000);
			}

		}
	});


});

$('#user-submenu').on('click','#btnEditarUser',function(){
		$('#EditarUser').modal('show');
		
	});
	
});