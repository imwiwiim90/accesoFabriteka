window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');

var Python = require('./js/python_js');
var python = new Python();

$(document).ready(function() {
  console.log('ready')

  $('#btn-entrance').on('click',function() {
    window.location.href = './entrance.html';
  })
});

