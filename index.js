var express = require('express')
var app = express();
var path = require('path')
var bodyParser = require('body-parser')

var sqlite3 = require('sqlite3').verbose()
var db = new sqlite3.Database('/tmp/michael.db')

app.use('/static', express.static(__dirname))
app.set('port', (process.env.PORT || 5000))

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))

app.get('/', function (request, response) {
    response.sendFile(__dirname + '/static/query.html')
})

app.post('/query', function (request, response, next) {
	var gene_locus=request.body.gene_locus
	console.log("Query is: " + gene_locus)
	//response.end(gene_locus)
	next()
}, function (request, response) {
	var gene_locus=request.body.gene_locus
	sqlRequest = "SELECT id, gene_locus, seqid, start, end, strand FROM gene_model WHERE gene_locus='" + gene_locus + "'"
	db.query(sqlRequest, function showQuery(err, rows) {
		console.log(row.id, row.gene_locus, row.seqid, row.start, row.end, row.strand)
	})
//	response.end(gene_locus)
})

var template = 'Node app is running at localhost: {port~number}'
var txt = template.replace('{port~number}', app.get('port'))

app.listen(app.get('port'), function() {
    console.log(txt)
})
