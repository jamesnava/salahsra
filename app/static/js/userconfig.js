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

	$('#Apersona').click(function(){

		$.ajax({
			url:'/cfg/mostrarpersonal',
			type:'GET',
			success: function(response){
				alert('hola');
				$('#contenedoracceso').html(response);
				
			}
		});
	});


	
});