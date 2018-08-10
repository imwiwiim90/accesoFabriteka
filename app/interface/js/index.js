window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');
var PYTHON_ADDRS = '127.0.0.1';
var PYTHON_PORT  = '5000';

function verificarPin() {
  $.ajax({
    url: 'http://' + PYTHON_ADDRS + ':' + PYTHON_PORT + '/verificarPin',
    method: 'GET',
    data: {
      data: ['1234']
    },
    success: function(data) {
      alert(data);
    },
    error: function(data) {
      alert("error:" + data);
      console.log(data)
    }
  })
}

var Python = require('./js/python_js');
var python = new Python();



$('#btn').on('click',function() {
  python.functions.verificarPin('1234');
})




