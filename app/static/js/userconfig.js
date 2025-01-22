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

	
});