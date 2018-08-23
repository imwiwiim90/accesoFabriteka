window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');

var Python = require('./js/python_js');
var main = require('./js/main');
var python = new Python();

$(document).ready(function() {


function receiveRFID(rfid) {
	python.verificarPin(rfid,(response) => {	
		if (response == 'true') {
			python.obtenerPorPin(rfid, (response) => {
				var [type,name,phone,mail,cc] = JSON.parse(response);
				python.desasignarPinCliente(rfid, (response) => {	
						if (response == 'true') {
							fillExitInfo(cc);
							$('#container-get-rfid').hide();
							$('#container-info').show();
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
}
$('#btn-back').on('click',function() {
    window.location.href = './index.html';
})

main.getRFID($('#container-loading'));
function fillExitInfo(cc) {
	python.duracionConTarjeta(cc,(response) => {
		var [hours,minutes,seconds] = JSON.parse(response).split(':');
		$('#card-time').html(hours + 'h ' + minutes + 'm ' + seconds + 's')
	})

	python.logsInside(cc,(data) => {
		console.log(data)
		var logs = JSON.parse(data);
		var seconds = 0;
		for (var i = 0; i + 1 < logs.length; i+=2) {
			var entrance = new Date(logs[i].datetime);
			var exit = new Date(logs[i+1].datetime);
		 	seconds += (exit - entrance)/1000;
		}
		var hours = Math.floor(seconds/(60*60));
		seconds = seconds%(60*60);
		var minutes = Math.floor(seconds/(60));
		seconds = Math.floor(seconds%60);
		$('#time-inside').html(hours + 'h ' + minutes + 'm ' + seconds + 's')
	});
}




main.listenRFID(receiveRFID);

});