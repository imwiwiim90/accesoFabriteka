window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');

var Python = require('./js/python_js');
var main = require('./js/main');
var python = new Python();

$(document).ready(function() {
	$('#container-get-rfid').hide();


	function receiveRFID(rfid) {
		python.verificarPin(rfid, (response) => {
			if (response == 'true') {
				alert('Este pin ya esta asignado');
				return
			}
			python.asignarPinCliente(rfid,id_,(response) => {
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

  /*
  var id_;
  $('#btn-check-id').on('click',function() {
  		id_ = $('#inpt-cc').val();

  		if (!id_.match(/^\d+$/g)) {
  			alert('La cedula sólo puede contener números');
  			return;
  		}

  		python.verificarCedulaCliente(id_,(response) => {
  			if (response == '3') idNotFound(id_);
  			if (response == '2') saveRFID();
  			if (response == '1') hasRFID();
  		});	
  		//idNotFound(id_);
  });
  */

  $('#btn-submit-info').on('click',function() {

  		var cc = $('#cc').val();
  		var name = $('#name').val();
  		var phone = $('#phone').val();
  		var mail = $('#mail').val();

  		if (!cc.match(/^\d+$/g)) {
  			alert('La cedula sólo puede contener números');
  			return;
  		}


  		console.log([cc,name,phone,mail]);
  		return
  		python.nuevoCliente(cc,name,phone,mail,(response) => {
  			saveRFID();
  		});
  });
});

