window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');

var Python = require('./js/python_js');
var python = new Python();

$(document).ready(function() {
	$('#client-info').hide();

	function idNotFound(id_) {
		$('#title-cc').html(id_);
		$('#client-id').slideUp();
		$('#client-info').show('slow');
	}

  $('#btn-back').on('click',function() {
    window.location.href = './index.html';
  })

  $('#btn-check-id').on('click',function() {
  		var id_ = $('#inpt-cc').val();
  		idNotFound(id_);
  });
});

