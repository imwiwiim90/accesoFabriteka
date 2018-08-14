window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');

var Python = require('./js/python_js');
var main = require('./js/main');
var python = new Python();

$(document).ready(function() {
	$('#client-info').hide();
	$('#container-get-rfid').hide();


	function idNotFound(id_) {
		$('#title-cc').html(id_);
		$('#client-id').slideUp();
		$('#client-info').show('slow');
	}

	function saveRFID() {
		main.getRFID($('#container-loading'));
		$('#client-info').slideUp()
		setTimeout(() =>  $('#container-get-rfid').slideDown(),500);

	}

  $('#btn-back').on('click',function() {
    window.location.href = './index.html';
  })

  $('#btn-check-id').on('click',function() {
  		var id_ = $('#inpt-cc').val();
  		idNotFound(id_);
  });

  $('#btn-submit-info').on('click',saveRFID)
});

