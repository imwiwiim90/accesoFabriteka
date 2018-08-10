class PythonJS {
	constructor() {
		console.log('contructed')
		var functions_name = ['verificarPin'];


		var functions = {};
		var self = this;
		for (var i = 0; i < functions_name.length; i++) {
			var name = functions_name[i];
			functions[functions_name[i]] = function() {
				var arguments_ = [];
				for (var j = 0; j < arguments.length; j++) arguments_.push(arguments[j]);

				$.ajax({
					method: 'GET',
					data: {
						data: arguments_,
					},
					url: 'http://127.0.0.1:5000/' + name,
					success(response) {
						console.log(response)
					},
					error(response) {
						console.log(response)
					}
				})
			}
		}
		this.functions = functions;
	}
}

module.exports = PythonJS;