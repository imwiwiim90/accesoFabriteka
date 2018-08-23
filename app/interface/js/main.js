
var python = new Python()

function getRFID($container) {
	console.log($container);
	$container.load('./html/gear.html');
	var $link = $('<link>');
	$link.attr('href','./css/loading.css')
	$link.attr('type',"text/css");
	$link.attr('rel',"stylesheet");
	$('head').append($link);
}

function iterativeGetPin(pin,callback) {
	if (!pin || pin == 'null') 
		 setTimeout(() => {
			python.getPin((pin) => {
				iterativeGetPin(JSON.parse(pin),callback)
			})
		},1000)
	else callback(pin)
}

function listenRFID(callback) {
	python.clearModule(() => {
		iterativeGetPin('',callback)
	})
}

exports.getRFID = getRFID;
exports.listenRFID = listenRFID;