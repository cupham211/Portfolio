var express = require('express');
var mysql = require('./dbcon.js');
var CORS = require('cors');

var app = express();
var handlebars = require('express-handlebars').create({defaultLayout:'main'});

app.use(express.json());
app.use(express.urlencoded({extended: true}));
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');
// ex: node server.js 6969 --will run on port 6969
app.set('port', process.argv[2]);
app.use(CORS());
app.set('mysql', mysql);
app.use('/plantwatch', require('./plantwatchServer.js'));

app.get('/', function(req, res, next){
    res.status(200);
    res.send('server running!');
})

app.use(function(req,res){
  res.status(404);
  res.render('404');
});

app.use(function(err, req, res, next){
  console.error(err.stack);
  res.status(500);
  res.render('500');
});
//flip2 port 6969
app.listen(app.get('port'), function(){
  console.log('Express started on http://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
});
