var http = require('http');
var fs = require('fs');
http.createServer(function(req, res){
	fs.readFile('read-html.html', function(err, data){
		res.writeHead(200, {'Content-Type':'text/html'});
		res.write(data);
		res.end('ok');
	});
}).listen(8080);
