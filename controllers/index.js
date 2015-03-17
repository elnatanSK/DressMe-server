var express = require('express');
var router = express.Router();




/*
 * top level routes
 */
router.get('/', function(req, res) {
        res.json({ message: 'Welcome to the DressMe API' });
});


/*
 * expose the router we create so that we can access it from
 * the top-level app.js
 */
module.exports = router
