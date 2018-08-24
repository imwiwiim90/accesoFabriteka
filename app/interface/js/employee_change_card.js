window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');

var Python = require('./js/python_js');
var main = require('./js/main');
var python = new Python();

$(document).ready(function() {
	$('#container-get-rfid').hide();
	$('#container-is-not-employee').hide();


	function receiveRFID(rfid) {
		python.verificarPin(rfid, (response) => {
			if (response == 'true') {
				alert('Esta tarjeta ya esta asignada');
				main.listenRFID(receiveRFID);
				return;
			}
			python.cambiarPinEmpleado(id_,rfid,(response) => {
				alert('Transacción exitosa');
    			window.location.href = './index.html';
			});
		});
	}

	function idNotFound(id_) {
		$('#title-cc').html(id_);
		$('#employee-id').slideUp();
		$('#container-is-not-employee').show('slow');
	}

	function saveRFID() {
		main.getRFID($('#container-loading'));
		main.listenRFID(receiveRFID);
		$('#employee-id').slideUp();
		setTimeout(() =>  $('#container-get-rfid').slideDown(),500);
	}

  var id_;
  $('#btn-check-id').on('click',function() {
  		id_ = $('#inpt-cc').val();

  		if (!id_.match(/^\d+$/g)) {
  			alert('La cédula sólo puede contener números');
  			return;
  		}

  		python.verificarCedulaEmpleado(id_,(response) => {
  			if (response == 'false') return idNotFound(id_)
  			saveRFID();
  		});	
  		//idNotFound(id_);
  });

  $('#btn-submit-info').on('click',function() {
  		var cc = id_;
  		var name = $('#name').val();
  		var phone = $('#phone').val();
  		var mail = $('#mail').val();
  		
  		python.nuevoCliente(cc,name,phone,mail,(response) => {
  			saveRFID();
  		});
  });
});

