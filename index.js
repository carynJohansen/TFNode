//set up connection with database
var sqlite3 = require('sqlite3').verbose()
var db = new sqlite3.Database('/tmp/michael.db')

db.serialize(function() {
	console.log("This is the serialize statement.")
})

//begin express app
var express = require('express')
var app = express()
var stylus = require('stylus')

var path = require('path')
var bodyParser = require('body-parser')

app.set('port', (process.env.PORT || 5000))
app.set('views', __dirname, + '/views')
app.set('view engine', 'jade')

//app.use(express.logger('dev'))
app.use('/static', express.static(__dirname))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))

/// catch 404 and forward to error handler
//app.use(function(request, response, next) {
//	var err = new Error('Not Found')
//	err.status = 404
//	next(err)
//})

app.get('/', function (request, response) {
    response.sendFile(__dirname + '/static/query.html')
})

app.post('/query', function (request, response, next) {
	db.serialize( function() {
		var reqGL = request.body.gene_locus,
		sql_query = "SELECT gm.id as gmID, gm.gene_locus, inter.regulator, inter.target \
		FROM gene_model as gm, interaction_network as inter \
		WHERE gm.gene_locus=? AND inter.regulator=gm.id"

	console.log("Query is: " + reqGL)
	counter = 1
	db.get(sql_query, reqGL, function(err, row) {
		if (err) {
			console.err(err)
		}
		else {
			response.json({"gm_locus" : row.gene_locus, "regulator" : row.regulator, "target" : row.target, "Count" : counter})
			//console.log("gm_locus: " + row.gene_locus + "\nRegulator: " + row.regulator + "\nTarget: " + row.target + "\nCounter: " + counter + "\n")
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
}) //close app.post

var template = 'Node app is running at localhost: {port~number}'
var txt = template.replace('{port~number}', app.get('port'))

app.listen(app.get('port'), function() {
    console.log(txt)
})
