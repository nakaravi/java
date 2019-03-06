//const express = require('express');
const router = express.Router();
var Db = require('mongodb').Db,
    MongoClient = require('mongodb').MongoClient,
    Server = require('mongodb').Server,
    ReplSetServers = require('mongodb').ReplSetServers,
    ObjectID = require('mongodb').ObjectID,
    Binary = require('mongodb').Binary,
    GridStore = require('mongodb').GridStore,
    Grid = require('mongodb').Grid,
    Code = require('mongodb').Code,
    assert = require('assert');

//var connection = mysql.createConnection('mysql://user:pass@host/db?debug=true&charset=BIG5_CHINESE_CI&timezone=-0700');


//get all records
router.get('/', (req, res) => {

	var db = new Db('api', new Server('localhost', 27017));
		
	
	db.collections('products', (err, collection)=>{
		
		/*collection.insertOne({id:3,name:'DELL',description:'Dell products'}, function(err, result) {
		console.log('aaaaaaaaaaaaaaa',err, result);
		});*/
		collection.find(1,1,true).toArray((err, items)=>{
			console.log(items.length);
				if(err) console.log(err);
				console.log(items);
				res.json({result:'success'});
			});
		});
	
	//res.json({result:'success'});
	/*
	const Test = mongoCon.collection('products');
	console.log(Test);
	
	/*.then((err, db)=>{
		
		db.collection('products', (err, collection)=>{
			collection.find().toArray((err, items)=>{
				if(err) throw err;
				console.log(items);
				res.json(items);
			});
		});
	});*/
	
});

//get single records using parameter.
router.get('/:id',(req, res)=>{
	console.log('inside', req.params.id);
	let id = req.params.id;
	connection.query('SELECT * from products where id='+id, function (error, results, fields) {
		if (error) throw error;
		var resultJson = JSON.stringify(results);
		resultJson = JSON.parse(resultJson);
		var apiResult = {
			result:'success'
		};
		
		apiResult.data = resultJson;
				
		res.json(apiResult);
		
	});

});

//post records and insert to db
router.post('/',(req, res)=>{
	//console.log('post content.................',req);
	let qry = 'insert into products (name, description, price, category_id) values ("' + req.body.name +'","'+ req.body.description+'","'+ req.body.price+'","1")';
	console.log(qry);
	connection.query(qry, (error, results, fields) => {
		if(error) throw error;
		var resultJson = JSON.stringify(results);
		var apiResult = {
			result:'success'
		};
		
		apiResult.data = resultJson;
				
		res.json(apiResult);
	});
	
});
//update records
router.patch('/:id', function(req, res) { });

//delete record using id
router.delete('/:id',(req, res)=>{
	connection.query('delete from products where id' + id, function(error, results, fields){
		if(error) throw error;
		var resultJson = JSON.stringify(results);
		resultJson = JSON.parse(resultJson);
		var apiResult = {
			result:'success'
		};
		
		apiResult.data = resultJson;
				
		res.json(apiResult); 
	});

});

/* GET api listing. */


module.exports = router;


