
const express = require('express');
const router = express.Router();
const data = [{id:1,'class':'skelton'},{id:2,'class':'skelton'},{id:3,'class':'skelton'},{id:4,'class':'skelton'},{id:5,'class':'skelton'},{id:1,'class':'skelton'},{id:2,'class':'skelton'},{id:3,'class':'skelton'},{id:4,'class':'skelton'},{id:5,'class':'skelton'}];
const data1 = [{id:1,'class':'skelton'}];
/* GET api listing. */
router.get('/', (req, res) => {
  res.send(JSON.stringify(data));
});

module.exports = router;
