window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');

var Python = require('./js/python_js');
var main = require('./js/main');
var python = new Python();

$(document).ready(function() {

function getRFID() {
	return $('#input-rfid').val();
}
$('#btn-rfid').on('click',() => {
	var rfid = getRFID();
	python.verificarPin(rfid,(response) => {	
		if (response == 'true') {
			python.obtenerPorPin(rfid, (response) => {
				var [type,name,phone,mail,cc] = JSON.parse(response);
				python.desasignarPinCliente(rfid, (response) => {	
						if (response == 'true') {
							python.duracionConTarjeta(cc,(response) => {
								alert(response);
							})
							$('container-get-rfid').hide();
							$('container-info').show();
						} else {
							alert('Hubo un problema en el sistema');
							window.location.href = './index.html';
						}
				});
			});	

		} else {
			alert('La tarjeta no se encuentra en el sistema');
			window.location.href = './index.html';
		}
	})


})

});