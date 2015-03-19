/*
 * configure our express app
 *
 *      use the body parser to parse json
 *      set default port to 8080
 */
var express     = require('express');
var app         = express();
var bodyParser  = require('body-parser');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var port = process.env.PORT || 8080;




/*
 * load app middleware
 */
app.use(require('./middlewares'));




/*
 * Register Routes found in controllers
 *
 *      All routes are based at /api
 */
app.use('/api', require('./controllers'));




/*
 * actually start the server
 */
var server = app.listen(port, function () {

      var host = server.address().address;
      var port = server.address().port;

      console.log('DressMe app listening at http://%s:%s', host, port);
});
