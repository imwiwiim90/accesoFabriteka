function getRFID($container) {
	console.log($container);
	$container.load('./html/gear.html');
	var $link = $('<link>');
	$link.attr('href','./css/loading.css')
	$link.attr('type',"text/css");
	$link.attr('rel',"stylesheet");
	$('head').append($link);
}

exports.getRFID = getRFID;