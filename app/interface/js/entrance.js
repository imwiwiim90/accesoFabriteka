window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');

var Python = require('./js/python_js');
var main = require('./js/main');
var python = new Python();

$(document).ready(function() {
	$('#client-info').hide();
	$('#container-get-rfid').hide();
	$('#client-has-rfid').hide();


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

	function idNotFound(id_) {
		$('#title-cc').html(id_);
		$('#client-id').slideUp();
		$('#client-info').show('slow');
	}

	function saveRFID() {
		main.getRFID($('#container-loading'));
		main.listenRFID(receiveRFID);
		$('#client-id').slideUp();
		$('#client-info').slideUp();
		setTimeout(() =>  $('#container-get-rfid').slideDown(),500);
	}

	function hasRFID() {
		$('#client-id').slideUp();
		$('#client-info').slideUp();
		$('#client-has-rfid').slideDown();
	}

  $('#btn-back').on('click',function() {
    window.location.href = './index.html';
  })

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

