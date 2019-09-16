//const express = require('express');
const router = express.Router();
bson = require('../../node_modules/bson/browser_build/bson');
/*var Db = require('mongodb').Db,
    MongoClient = require('mongodb').MongoClient,
    Server = require('mongodb').Server,
    ReplSetServers = require('mongodb').ReplSetServers,
    ObjectID = require('mongodb').ObjectID,
    Binary = require('mongodb').Binary,
    GridStore = require('mongodb').GridStore,
    Grid = require('mongodb').Grid,
    Code = require('mongodb').Code,
    assert = require('assert');*/

//var connection = mysql.createConnection('mysql://user:pass@host/db?debug=true&charset=BIG5_CHINESE_CI&timezone=-0700');

	//var mongoclient = new MongoClient(new Server("localhost", 27017), {native_parser: true});

var mc = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017";

//get all records
router.get('/', (req, res) => {
	var  ary = [];

	
	

	mc.connect(url, function(err, db) {
		if (err) throw err;
	
		var dbo = db.db("api");
		dbo.collection("products").find().toArray((err, items)=>{
			
			if(err){res.json({result:'failure', data:[]});}
			
			items.forEach(item=>{
				
				ary.push(item);
			})
			res.json({result:'success', data:JSON.parse(JSON.stringify(ary))});
		
		})
	
	});
	
	
});
router.get('/:search',(req, res)=>{
	console.log('inside', req.params.id);
	let txt = req.params.search;
	var ary = [];
	mc.connect(url, (err, db)=>{
		var q = {name:txt}
		//var query = { name: /^S/ };
		//db.users.find({"name": /.*m.*/})
		//or, similar:
		//db.users.find({"name": /m/})
		db.db("api").collection("products").find(q).toArray((err, items)=>{
			
			if(err){res.json({result:'failure', data:[]});}
			
			items.forEach(item=>{
				
				ary.push(item);
			})
			res.json({result:'success', data:JSON.parse(JSON.stringify(ary))});
		
		})

	})
});


//get single records using parameter.
router.get('/:id',(req, res)=>{
	console.log('inside', req.params.id);
	let id = req.params.id;
	var ary = [];
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
	let qry = 'insert into products (name, description) values ("' + req.body.name +'","'+ req.body.description+'")';
	let json = {name:req.body.name, description:req.body.description};
	mc.connect(url, (err, db)=>{

		db.db("api").collection("products").insert(json,(err, data)=>{
			console.log(data)
		})
		res.json({result:"success"});
	});
});
//update records
router.patch('/:id', function(req, res) { 
	let json = {name:req.body.name, description:req.body.description};
	var myquery = { name: "HP" };
	var newvalues = { $set: {name: "Mickey", description: "Canyon 123" } };
	mc.connect(url, (err, db)=>{

		db.db("api").collection("products").updateOne(myquery, newvalues,(err, data)=>{
			console.log(data)
		})
		res.json({result:"success"});
	});
	
});

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


