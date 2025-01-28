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


	
});