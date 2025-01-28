$(document).ready(function(){

$('#btnupdatetrama,#btnupdatepersonal,#btnupdateregistrador').click(function(event){
	var elemgenerador=$(event.target);
	var idgenerador=elemgenerador.attr('id')
	$('#dateup').val(idgenerador);	
	$('#modalupdatedata').modal('show');
});

$('#update').on('click',function(){
	//recuperando el archivo
	const filesinput=$('#myFile')[0];
	const file=filesinput.files[0];
	var identificador=$('#dateup').val();
	if(!file){
		alert('Seleccione un archivo');
		return;
	}

	const formData = new FormData();
    formData.append('filename', file);
    formData.append('identificador',identificador)
    
    $.ajax({
    	url:'/medico/updateData',
    	type:'POST',
    	data:formData,
    	processData:false,
    	contentType:false,
    	success: function(response){
    	var modal=bootstrap.Modal.getInstance(document.getElementById('modalupdatedata'));
        modal.hide();
        alert('Ser insertó '+response+' datos')
    	}

    });
});

});