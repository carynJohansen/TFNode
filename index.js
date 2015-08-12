//environment
var express = require('express')
var app = express()
var stylus = require('stylus')
var http = require('http')
var path = require('path')
var bodyParser = require('body-parser')
var fs = require('fs')
var jade = require('jade')
var Glob = require('glob')

//Database connection
var sqlite3 = require('sqlite3').verbose()
var db = new sqlite3.Database('/tmp/michael.db')

app.set('port', (process.env.PORT || 5000))
app.set('views', path.join(__dirname, 'views'))
app.set('view engine', 'jade')

//app.use(express.logger('dev'))
app.use(express.static(__dirname + '/static'))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: false }))

/// catch 404 and forward to error handler
//app.use(function(request, response, next) {
//	var err = new Error('Not Found')
//	err.status = 404
//	next(err)
//})

app.get('/', function (request, response) {
    response.sendFile(__dirname + '/views/query.html')
})

app.post('/query', function (request, response, next) {
	function showRegulator(results, gene) {
		//here, gene is a string and results is an array of JSON objects (it itself is an object)
		var images = geneImages()
		console.log("this is images: " + images)
		response.render('result', { gene: gene, data : results, plots : images })
	} //close showRegulator

	function queryByRegulator(whenDone) {
		
		db.serialize( function() {
			var reqGL = request.body.gene_locus
			var sql_query = "SELECT gm2.gene_locus as target_locus, \
			inter.int_id as interaction_id, \
			gm2.id as gmID, inter.target as target_id \
			FROM interaction_network as inter \
			INNER JOIN gene_model as gm1 ON (inter.regulator = gm1.id) \
			INNER JOIN gene_model as gm2 ON (inter.target=gm2.id) \
			WHERE (gm1.gene_locus=?)"
			console.log("Query is: " + reqGL)

			db.all(sql_query, reqGL, function(err, rows) {
				if (err) {
					console.log(err)
				} else {
					whenDone(rows, reqGL)
				} //close ifelse
			}) //close db.all
		}) // close serialize
	} // close queryByRegulator

	function geneImages() {
		//return an array of files associated with the searched for gene
		gpattern = request.body.gene_locus
		console.log("In geneImages(). here's the gene: " + gpattern)
		var ts = new Glob("/static/images/[reqGL]", function(err, files) { 
			if (err) {
				console.log(err)
			} else {
				console.log("files: " + files)
			}
		}) //close glob
		console.log("after")
	}//close geneImages

	var im = geneImages()
	console.log("var image : " + im)
	queryByRegulator(showRegulator)
}) //close app.post

var template = 'Node app is running at localhost: {port~number}'
var txt = template.replace('{port~number}', app.get('port'))

app.listen(app.get('port'), function() {
    console.log(txt)
})


