var express     = require('express');
var bodyParser  = require('body-parser');



/*
 * configure our express app
 *
 *      use the body parser to parse json
 *      set default port to 8080
 */
var app         = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port = process.env.PORT || 8080;



/*
 * Routes
 */
var router = express.Router();

router.get('/', function(req, res) {
        res.json({ message: 'Welcome to the DressMe API' });
});



/*
 * Register Routes
 *
 *      All routes are based at /api
 */
app.use('/api', router);



/*
 * actually start the server
 */
var server = app.listen(port, function () {

      var host = server.address().address
      var port = server.address().port

      console.log('DressMe app listening at http://%s:%s', host, port)
});
