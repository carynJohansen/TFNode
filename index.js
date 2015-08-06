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
app.set('views', path.join(__dirname, 'views'))
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
    response.sendFile(__dirname + '/views/query.html')
})

app.post('/query', function (request, response, next) {

<<<<<<< HEAD
	console.log("Query is: " + reqGL)
	counter = 1
	db.all(sql_query, reqGL, function(err, rows) {
		if (err) {
			console.err(err)
		}
		else {
			response.end(JSON.stringify(rows)) //this returns an array of JSON objects
			counter = counter + 1
		}
//		db.get("SELECT gm.gene_locus, inter.regulator, inter.target \
//			FROM gene_model as gm, interaction_network as inter \
//			WHERE gm.gene_locus=? AND inter.regulator=?", [gene_locus, gene_locus], function(err, row) {
//				if (err) {
//					console.err(err)
//				} else{
//					response.json({"gm_locus" : row.gene_locus, "regulator" : row.regulator, "target" : row.target})
//				}
//			})
		}) //close db.all/get
	}) // close db.serialize
=======
	function showRegulator(results) {
		console.log("In showRegulator")
		//response.end(JSON.stringify(results))
		response.render('result', { data : results })
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
					console.log("after whenDone callback")
				} //close ifelse
			}) //close db.all
		}) // close serialize
	} // close queryByRegulator
	queryByRegulator(showRegulator)
>>>>>>> callbacks
}) //close app.post

var template = 'Node app is running at localhost: {port~number}'
var txt = template.replace('{port~number}', app.get('port'))

app.listen(app.get('port'), function() {
    console.log(txt)
})


