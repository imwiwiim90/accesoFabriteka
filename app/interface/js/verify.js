window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');
var Python = require('./js/python_js');
var main = require('./js/main');
var python = new Python();

$(document).ready(function() {
	main.getRFID($('#container-loading'));
	$('#btn-back').on('click',function() {
    window.location.href = './index.html';
  })
});
