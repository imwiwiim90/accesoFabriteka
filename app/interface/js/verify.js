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
			if (response == 'false') showContainer('container-not-found');
			else {
				python.obtenerPorPin(rfid, (response) => {
					var [type,name,phone,mail,cc] = JSON.parse(response);
					type = (type == 'cliente' ? 'Cliente' : 'Empleado')
					$('#info-type').html(type);
					$('#info-name').html(name);
					$('#info-cc').html(cc);
					$('#info-mail').html(mail);
					$('#info-phone').html(phone);
					showContainer('container-info');
				})
			}
		});	
	})


	main.getRFID($('#container-loading'));
	$('#btn-back').on('click',function() {
	    window.location.href = './index.html';
	})

	var containers = ['container-get-rfid','container-not-found','container-info'];
	function showContainer(container) {
		console.log(container)
		containers.forEach((c) => $('#'+c).hide());
		$('#'+container).show();
	}

	$('#btn-again').on('click',() => showContainer('container-get-rfid'))
});
