//const express = require('express');
const router = express.Router();

//var connection = mysql.createConnection('mysql://user:pass@host/db?debug=true&charset=BIG5_CHINESE_CI&timezone=-0700');

 
connection.query('SELECT * from products', function (error, results, fields) {
	if (error) throw error;
	var resultJson = JSON.stringify(results);
	resultJson = JSON.parse(resultJson);
	var apiResult = {
		result:'success'
	};
	
	apiResult.data = resultJson;
            
	//send JSON to Express
	//res.json(apiResult);
	router.get('/', (req, res) => {
	  //res.json(apiResult);
	  res.json(apiResult);
	});
});



/* GET api listing. */


module.exports = router;


