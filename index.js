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
	var gene_locus=request.body.gene_locus,
		sql_query = "SELECT gm.id, gm.gene_locus, inter.regulator, inter.target \
	FROM gene_model as gm, interaction_network as inter \
	WHERE gm.gene_locus=? AND inter.regulator=?",
		params = []

	params.push(gene_locus, gene_locus)
	console.log("Query is: " + gene_locus)
	console.log("The query params are: " + params)
	db.get(sql_query, params, function(err, row) {
		if (err) {
			console.err(err)
		}
		else {
			response.json({"gm_locus" : row.gene_locus, "regulator" : row.regulator, "target" : row.target})
		}
//	db.get("SELECT gm.gene_locus, inter.regulator, inter.target \
//		FROM gene_model as gm, interaction_network as inter \
//		WHERE gm.gene_locus=? AND inter.regulator=?", [gene_locus, gene_locus], function(err, row) {
//			if (err) {
//				console.err(err)
//			} else{
//				response.json({"gm_locus" : row.gene_locus, "regulator" : row.regulator, "target" : row.target})
//			}
//		})
	})
	//response.end(gene_locus)
//	next()
//}, function (request, response) {
//	var gene_locus=request.body.gene_locus
//	sqlRequest = "SELECT id, gene_locus, seqid, start, end, strand FROM gene_model WHERE gene_locus='" + gene_locus + "'"
//	//db.query(sqlRequest, function showQuery(err, rows) {
//	//	console.log(row.id, row.gene_locus, row.seqid, row.start, row.end, row.strand)
//	console.log(gene_locus)
//	response.end("You want to query the database for: " + gene_locus)
//	response.end(gene_locus)
})

var template = 'Node app is running at localhost: {port~number}'
var txt = template.replace('{port~number}', app.get('port'))

app.listen(app.get('port'), function() {
    console.log(txt)
})
