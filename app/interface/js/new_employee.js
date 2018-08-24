window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');

var Python = require('./js/python_js');
var main = require('./js/main');
var python = new Python();

$(document).ready(function() {
  	var cc,name,phone,mail;
	$('#container-get-rfid').hide();


	function receiveRFID(rfid) {
		python.verificarPin(rfid, (response) => {
			if (response == 'true') {
				alert('Este pin ya esta asignado');
				return
			}
			python.nuevoEmpleado(rfid,cc,name,phone,mail,(response) => {
				alert('Transacción exitosa');
    			window.location.href = './index.html';
			});
		});
	}


	function saveRFID() {
		main.getRFID($('#container-loading'));
		main.listenRFID(receiveRFID);
		$('#client-id').slideUp();
		$('#client-info').slideUp();
		setTimeout(() =>  $('#container-get-rfid').slideDown(),500);
	}
	// TODO
	function hasRFID() {
		$('#client-id').slideUp();
		$('#client-info').slideUp();
		$('#client-has-rfid').slideDown();
	}


 // [pin, cedula, nombre, telefono, correo]

  
  $('#btn-submit-info').on('click',function() {

  		cc = $('#cc').val();
  		name = $('#name').val();
  		phone = $('#phone').val();
  		mail = $('#mail').val();

  		if (!cc.match(/^\d+$/g)) {
  			alert('La cedula sólo puede contener números');
  			return;
  		}

  		python.verificarCedulaCliente(cc, (response) => {
  			if (response != 3) {
  				alert('La cédula ya esta asignada a un cliente');
  				return;
  			}

  			python.verificarCedulaEmpleado(cc, (exists) => {
  				if (exists == 'true') {
  					alert('La cédula ya está asignada a un empleado');
  					return;
  				}
  				saveRFID();
  			});
  		})

  		console.log([cc,name,phone,mail]);

  });
});

