window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');

var Python = require('./js/python_js');
var main = require('./js/main');
var python = new Python();

$(document).ready(function() {
	$('#container-get-rfid').hide();
	$('#container-is-not-client').hide();
	$('#container-not-card').hide();


	function receiveRFID(rfid) {
		python.verificarPin(rfid, (response) => {
			if (response == 'true') {
				alert('Esta tarjeta ya esta asignada');
				main.listenRFID(receiveRFID);
				return;
			}
			python.cambiarPinCliente(id_,rfid,(response) => {
				alert('Transacción exitosa');
    			window.location.href = './index.html';
			});
		});
	}

	function idNotFound(id_) {
		$('#title-cc').html(id_);
		$('#client-id').slideUp();
		$('#container-is-not-client').show('slow');
	}

	function notCard(id_) {
		$('#client-id').slideUp();
		$('#container-not-card').show('slow');
	}

	function saveRFID() {
		main.getRFID($('#container-loading'));
		main.listenRFID(receiveRFID);
		$('#client-id').slideUp();
		setTimeout(() =>  $('#container-get-rfid').slideDown(),500);
	}

  var id_;
  $('#btn-check-id').on('click',function() {
  		id_ = $('#inpt-cc').val();

  		if (!id_.match(/^\d+$/g)) {
  			alert('La cédula sólo puede contener números');
  			return;
  		}

  		python.verificarCedulaCliente(id_,(response) => {
  			if (response == 3) return idNotFound(id_)
  			if (response == 2) return notCard(id_)
  			saveRFID();
  		});	
  });
});

