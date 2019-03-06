// Get dependencies
//var connection = mysql.createConnection('mysql://user:pass@host/db?debug=true&charset=BIG5_CHINESE_CI&timezone=-0700');
//const express = require('express');
global.express 		= require('express');
global.path 		= require('path');
global.http 		= require('http');
global.cors 		= require('cors');
global.bodyParser 	= require('body-parser');
global.mysql      	= require('mysql');

global.connection 	= mysql.createConnection({ 
	host:"localhost",
	user: "root", 
	password: "", 
	database: "api"
});

global.mongoClient	= require('mongodb').MongoClient;
mongoClient.connect('mongodb://localhost:27017/abi',{ useNewUrlParser: true });
global.mongoCon		= mongoClient.connection;
global.schema		= mongoClient.Schema;

// Get our API routes
const mproducts 	= require('./server/routes/mproducts');
const products 	= require('./server/routes/products');
const api 		= require('./server/routes/api');
const data 		= require('./server/routes/data');
const app 		= express();

var bodyParser 	= require('body-parser');


// Parsers for POST data
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.json({ type: 'application/json' }));
app.use(bodyParser.urlencoded({ extended: false }));

// Point static path to dist
app.use(express.static(path.join(__dirname, 'fractal')));

// Set our api routes
app.use('/mproducts', mproducts);
app.use('/products', products);
app.use('/api', api);
app.use('/data', data);
app.use('/views', express.static(__dirname +'/views')); 
// Catch all other routes and return the index file
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'views/index.html'));
});

/**
 * Get port from environment and store in Express.
 */
const port = process.env.PORT || '3000';
app.set('port', port);

/*buffer checking*/
const buf = Buffer.alloc(5,'b');
console.log(buf);

/**
 * Create HTTP server.
 */
const server = http.createServer(app);

/**
 * Listen on provided port, on all network interfaces.
 */
server.listen(port, () => console.log(`API running on localhost:${port}`));
