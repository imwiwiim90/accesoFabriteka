window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');

var Python = require('./js/python_js');
var python = new Python();


var tests = {
	nuevoCliente : function() {
		python.nuevoCliente('102020000','wallace','302323222','wia@c.com');
		python.nuevoCliente('102020120','wallas','30343323222','w@c.com');
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
	},
	cambiarPinEmpleado: function() {
		python.cambiarPinEmpleado('1020339494','12DFCAMBEDE12')
	},
	asignarPinCliente: function() {
		python.asignarPinCliente('12EEDDNEW2321','102020000');
	},
	cambiarPinCliente: function() {
		python.cambiarPinCliente('102020000','12EEDDCAMB2321');
	},
	obtenerClientePorPin: function() {
		python.obtenerPorPin('12EEDDCAMB2321');
	},
	desasignarPinCliente: function() {
		python.desasignarPinCliente('12EEDDCAMB2321');
	},
	verificarCedulaEmpleado: function() {
		python.verificarCedulaEmpleado('120293233');
		python.verificarCedulaEmpleado('1020339494');
	}
}



$(document).ready(function() {
  console.log('ready')

  function btnOnClick(event) {
    id_ = $(event.target).attr('id').replace('btn-','');
    window.location.href = './' + id_ + '.html';
  }

  function setUsersWithCard() {
  	python.usuariosConTarjeta((users)=> {
  		if (users == 1) $('#clients-card').html('1 cliente');
  		else  $('#clients-card').html(users + ' clientes');
  		setTimeout(setUsersWithCard,5000);	
  	})
  }
  setUsersWithCard()

  $('#btn-entrance').on('click',btnOnClick)
  $('#btn-verify').on('click',btnOnClick)
  $('#btn-exit').on('click',btnOnClick)
  $('#btn-client_change_card').on('click',btnOnClick)

});

