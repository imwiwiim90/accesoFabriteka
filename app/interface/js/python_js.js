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
		];


		var functions = {};
		var self = this;
		for (var i = 0; i < functions_name.length; i++) {
			const url = 'http://127.0.0.1:5000/' + functions_name[i];
			self[functions_name[i]] = function() {
				var arguments_ = [];
				for (var j = 0; j < arguments.length; j++) arguments_.push(arguments[j]);

				$.ajax({
					method: 'GET',
					data: {
						data: arguments_,
					},
					url: url,
					success(response) {
						console.log(response)
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