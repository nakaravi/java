//const express = require('express');
const router = express.Router();

//var connection = mysql.createConnection('mysql://user:pass@host/db?debug=true&charset=BIG5_CHINESE_CI&timezone=-0700');


//get all records
router.get('/', (req, res) => {
	connection.query('SELECT * from products', function (error, results, fields) {
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


