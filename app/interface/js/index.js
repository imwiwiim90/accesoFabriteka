window.$ = window.jQuery = require('./node_modules/jquery/dist/jquery.min.js');

var Python = require('./js/python_js');
var python = new Python();


$(document).ready(function() {
  console.log('ready')

  function btnOnClick(event) {
    id_ = $(event.target).attr('id').replace('btn-','');
    window.location.href = './' + id_ + '.html';
  }

  $('#btn-entrance').on('click',btnOnClick)
  $('#btn-verify').on('click',btnOnClick)
  $('#btn-exit').on('click',btnOnClick)

});

