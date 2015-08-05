//environment
var express = require('express')
var app = express()
 stylus = require('stylus')
var http = require('http')
var path = require('path')
var bodyParser = require('body-parser')
var fs = require('fs')
var jade = require('jade')

//Database connection
var sqlite3 = require('sqlite3').verbose()
var db = new sqlite3.Database('/tmp/michael.db')

app.set('port', (process.env.PORT || 5000))
app.set('views', __dirname, + '/views')
app.set('view engine', 'jade')

//app.use(express.logger('dev'))
//app.use(express.static(__dirname + '/static'))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))

/// catch 404 and forward to error handler
//app.use(function(request, response, next) {
//	var err = new Error('Not Found')
//	err.status = 404
//	next(err)
//})



app.get('/', function (request, response) {
	var maintainer = {
		name: 'Person Person',
		twitter: '@PersonPerson',
		blog: 'personperson.com'
	}
	//response.render('static/jadeTemplate', maintainer)
	//response.render('views/index', {title: 'Hey', message : 'Hi!'})
    response.sendFile(__dirname + '/static/query.html')
})

app.post('/query', function (request, response, next) {

	function showRegulator(result) {
		response.end(JSON.stringify(result))
	} //close showRegulator

	function queryByRegulator(whenDone) {
		db.serialize( function() {

			var reqGL = request.body.gene_locus
			var sql_query = "SELECT gm.id as gmID, gm.gene_locus, inter.regulator, inter.target \
			FROM gene_model as gm, interaction_network as inter \
			WHERE gm.gene_locus=? AND inter.regulator=gm.id"
			console.log("Query is: " + reqGL)

			db.all(sql_query, reqGL, function(err, rows) {
				if (err) {
					console.log(err)
				} else {
					whenDone(rows)
				} //close ifelse
			}) //close db.all
		}) // close serialize
	} // close queryByRegulator
	queryByRegulator(showRegulator)
}) //close app.post

var template = 'Node app is running at localhost: {port~number}'
var txt = template.replace('{port~number}', app.get('port'))

app.listen(app.get('port'), function() {
    console.log(txt)
})


