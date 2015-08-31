//environment
var express = require('express')
var app = express()
var stylus = require('stylus')
var http = require('http')
var path = require('path')
var bodyParser = require('body-parser')
var fs = require('fs')
var jade = require('jade')
var globule = require('globule')
var util = require('util')

//Database connection
var sqlite3 = require('sqlite3').verbose()
var db = new sqlite3.Database('/Users/carynjohansen/Documents/NYUClasses/Purugganan_Lab/TFInteraction_db/michael.db')

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
		var im_path = []
		for ( i = 0 ; i < images.length; i ++) {
			im_path[i] = images[i].replace('static/', '')
		}
		console.log("this is images: " + images)
		console.log(typeof images[0] == 'string')
		response.render('layout', { gene: gene, data : results, plots : im_path })
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
		file_pattern = request.body.gene_locus 
		fs.exists('static/images/LOC_Os01g01840_032_000.png', function (exists) {
			util.debug(exists ? "it's there" : "nope, no image")
		})
		console.log("In geneImages(). here's the gene: " + file_pattern)
		var plot_files = globule.find("static/images/*" + file_pattern + "*")
		console.log("here's the paths for the image: " + plot_files)
		return plot_files
		//console.log("after globule")
	}//close geneImages

	queryByRegulator(showRegulator)
}) //close app.post

var template = 'Node app is running at localhost: {port~number}'
var txt = template.replace('{port~number}', app.get('port'))

app.listen(app.get('port'), function() {
    console.log(txt)
})


