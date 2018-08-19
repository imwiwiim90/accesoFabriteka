window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');

var Python = require('./js/python_js');
var python = new Python();


var tests = {
	nuevoCliente : function() {
		python.nuevoCliente('102020000','wallace','302323222','wia@c.com');
	},
	verificarCedulaCliente: function() {
		python.verificarCedulaCliente('102020000')
		python.verificarCedulaCliente('102020001')
	},
	nuevoEmpleado: function() {
		python.nuevoEmpleado('12DFF34EDE12','1020339494','Albertoso','3120002393','alberto@gmail.com')
		python.nuevoEmpleado('12DFF34343DD','1021210232','Robertina','3142220239','robertin@gmail.com')
	},
	borrarEmpleado: function() {
		python.borrarEmpleado('12DFF34343DD');
	}
}



$(document).ready(function() {
  console.log('ready')

  function btnOnClick(event) {
    //id_ = $(event.target).attr('id').replace('btn-','');
    //window.location.href = './' + id_ + '.html';
    tests.borrarEmpleado();
  }

  $('#btn-entrance').on('click',btnOnClick)
  $('#btn-verify').on('click',btnOnClick)
  $('#btn-exit').on('click',btnOnClick)

});

