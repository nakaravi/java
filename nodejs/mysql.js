// Include http module, 
var http = require('http'), 
// And mysql module you've just installed. 
	mysql = require("mysql"); 
	 
// Create the connection. 
// Data is default to new mysql installation and should be changed according to your configuration. 
var connection = mysql.createConnection({ 
	host:"localhost",
	user: "root", 
	password: "", 
	database: "api"
}); 
connection.connect();

connection.query('SELECT * from products', function (error, results, fields) {
  if (error) throw error;
  console.log('The solution is: ', results[0].name );
});
 
connection.end();


// Create the http server. 
var server = http.createServer(function (request, response) { 
	response.end('test');
});


	
	// Attach listener on end event. 
	server.on('end', function () {
		// Query the database. 
		connection.query('SELECT * FROM products;', function (error, rows, fields) { 
			response.writeHead(200, { 
				'Content-Type': 'x-application/json' 
			}); 
			// Send data as JSON string. 
			// Rows variable holds the result of the query. 
			response.end(JSON.stringify(rows)); 
		}); 
	}); 
// Listen on the 8080 port. 
server.listen(8080);



/*
var server = http.createServer(function (request, response) { 
	
	// Attach listener on end event. 
	request.on('end', function () { 
		// Query the database. 
		connection.query('SELECT * FROM quote;', function (error, rows, fields) { 
			response.writeHead(200, { 
				'Content-Type': 'x-application/json' 
			}); 
			// Send data as JSON string. 
			// Rows variable holds the result of the query. 
			response.end(JSON.stringify(rows)); 
		}); 
	}); 
// Listen on the 8080 port. 
}).listen(8080);
*/

