class PythonJS {
	constructor() {
		console.log('contructed')
		var functions_name = [
			'verificarPin',
			'nuevoCliente',
			'nuevoEmpleado',
			'verificarCedulaCliente',
			'borrarEmpleado', 
			'cambiarPinEmpleado',
			'cambiarPinCliente',
			'asignarPinCliente',
			'desasignarPinCliente',
			'obtenerPorPin',
			'verificarCedulaEmpleado',
			'entradasMensuales',
			'movimientosMes',
			'movimientosDia',
			'duracionConTarjeta',
			'clearModule',
			'getPin',
			'logsInside',
		];


		var functions = {};
		var self = this;
		for (var i = 0; i < functions_name.length; i++) {
			const url = 'http://127.0.0.1:5000/' + functions_name[i];
			self[functions_name[i]] = function() {
				var arguments_ = [];
				for (var j = 0; j < arguments.length; j++) arguments_.push(arguments[j]);
				var callback;
				if (typeof arguments[arguments.length-1] === 'function') callback = arguments_.pop();
				$.ajax({
					method: 'GET',
					data: {
						data: arguments_,
					},
					url: url,
					success(response) {
						callback(response);
					},
					error(response) {
						console.log(response)
					}
				})
			}
		}
	}
}

module.exports = PythonJS;