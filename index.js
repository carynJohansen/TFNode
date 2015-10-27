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
var child = require('child_process')

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
    response.render('query')
})

app.post('/query', function (request, response, next) {

	function showRegulator(results, reg_gene) {
		//here, gene is a string and results is an array of JSON objects (it itself is an object)
		var images = geneImages()
		var im_path = []
		for ( i = 0 ; i < images.length; i ++) {
			im_path[i] = images[i].replace('static/', '')
		}
		console.log("this is images: " + images)
		//console.log(typeof results == 'object') //this is true, results is an object
		var vcf = new Object()
		var genotypes
		var alleles
		//get the start and stop coordinates to regulator gene
		get_regulator_coordinates().then(function(rcJsonData) {
			return vcf_python(rcJsonData)
		}).then(function(vcfData) {
			vcf = JSON.parse(vcfData)
			return vcf_allele_counts()
		}).then(function(alleleData) {
			alleles = alleleData
			return vcf_genotype_counts()
		}).then(function(gtData) {
			genotypes = gtData
			response.render('firstresult', { gene: reg_gene, data : results, plots : im_path, variants: vcf, alleleC : alleles, gtC : genotypes })
		}).catch(function(reason) {
			console.log(reason)
		}) //close catch and promise chain
	} // close showRegulator



//		all([vcf_get(), vcf_allele_freqs()])
//			.then(function (lots) {
//				var vcfObj = new Object()
//				try {
//				//vcfObj = JSON.stringify(vcf)
//				vcfObj = JSON.parse(lots[0])
//				//console.log(vcf)
//				} catch (e) {
//					console.log('oh no error!')
//					console.log(e instanceof SyntaxError)
//					console.log(e.message)
//				} // close catch
//				response.render('firstresult', { gene: reg_gene, data : results, plots : im_path, variants: vcfObj, allele_counts : lots[1] })
//			}).catch(function(reason) {
//				console.log(reason)
//			})
		
		//response.render('firstresult', { gene: gene, data : results, plots : im_path })
	

	function showTarget(results, gene) {

	}

	function queryByRegulator(whenDone) {
		db.serialize( function() {
			var reqGL = request.body.reg_gene_locus
			var sql_query = "SELECT gm2.gene_locus as target_locus, \
			gm2.seqid as chromosome, \
			gm2.start as start, \
			gm2.end as end, \
			inter.in_prior as prior, \
			stats.var_exp_ranksum as rank \
			FROM interaction_network as inter \
			INNER JOIN gene_model as gm1 ON (inter.regulator = gm1.id) \
			INNER JOIN gene_model as gm2 ON (inter.target = gm2.id) \
			INNER JOIN interaction_stats as stats ON (stats.interaction_id = inter.int_id) \
			WHERE (gm1.gene_locus=?)"
			//console.log("Query (regulator) is: " + reqGL)

			db.all(sql_query, reqGL, function(err, rows) {
				if (err) {
					console.log(err)
				} else {
					//console.log(typeof rows == 'object')
					whenDone(rows, reqGL)
				} //close ifelse
			}) //close db.all
		}) // close serialize
	} // close queryByRegulator

	function queryByTarget(whenDone) {
		db.serialize( function () {
			var tarGL = request.body.tar_gene_locus
			var sql_query = "SELECT gm2.gene_locus as regulator_locus \
			FROM interaction_network as inter \
			INNER JOIN gene_model as gm1 ON (inter.target = gm1.id) \
			INNER JOIN gene_model as gm2 ON (inter.regulator = gm2.id) \
			where (gm1.gene_locus=?)"
			//console.log("Query (target) is: " + tarGL)

			db.all(sql_query, tarGL, function(err, rows) {
				if (err) {
					console.log(err) 
				} else {
					whenDone(rows, tarGL)
				} //close ifelse
			}) //close db.all
		}) //close db.serialize
	} //close queryByTarget

	function geneImages() {
		//return an array of files associated with the searched for gene
		file_pattern = request.body.reg_gene_locus 
		//fs.exists('static/images/LOC_Os01g01840_032_000.png', function (exists) {
		//	util.debug(exists ? "it's there" : "nope, no image")
		//})
		console.log("In geneImages(). here's the gene: " + file_pattern)
		var plot_files = globule.find("static/images/*" + file_pattern + "*")
		console.log("here's the paths for the image: " + plot_files)
		return plot_files
	}//close geneImages

	function get_regulator_coordinates() {
		return new Promise(function(resolve, reject) {
			db.serialize( function () {
				var regGL = request.body.reg_gene_locus
				var sql_query = "SELECT gm.start, gm.end, gm.seqid as chrom \
					FROM gene_model as gm \
					WHERE (gm.gene_locus = ?)"
				db.all(sql_query, regGL, function(err, rows) {
				//console.log("In db.all in get_coordinates()")
					if (err) {
						console.log(err)
					} else {
						//console.log(regGL)
						//console.log(rows[0])
						resolve(rows[0])
					}
				})//close db.all
			})//close db.serialize
		}) //close new promise
	}//close get_regulator_coordinates

	function vcf_get(coordJSON) {
		return new Promise(function(resolve, reject) {
			//console.log("in vcf_python")
			//coordinates is a JSON object with start and stop
			//console.log(coordinates)
			var start = coordJSON["start"]
			var end = coordJSON["end"]
			var chrom = coordJSON["chrom"]
<<<<<<< HEAD
=======
			console.log("start: " + start)
			console.log("end: " + end)
			console.log("chr: " + chrom)
>>>>>>> master

			var python = child.spawn('python',[ __dirname + '/database/vcf_get.py', chrom, start, end])
			var chunk = ''	

			python.stdout.on('data', function(data) {
				chunk += data
				//console.log(chunk)
				resolve(chunk)
			}) //close stdout.on
			//catch python error message:
			python.stderr.on('data', function (data) {
				console.log('python stderr: ' + data)
				response.end('python error! ' + data)
			})
		}) //close new promise
	} //close vcf_python

<<<<<<< HEAD
	function vcf_allele_counts() {
		return new Promise(function (fulfill, reject) {
			var gl = request.body.reg_gene_locus
			var python = child.spawn('python', [ __dirname + '/database/vcf_allele_freq.py', gl])
			var chunk = ''

			python.stdout.on('data', function (data) {
				chunk += data
				fulfill(chunk)
			}) //close stdout
			python.stderr.on('data', function (data) {
				console.log('python err: ' + data)
				response.end('python error in allele counts!' + data)
			}) //close stderr
		})//close promise
	} //close function

	function vcf_genotype_counts() {
		return new Promise(function (fulfill, reject) {
			var gl = request.body.reg_gene_locus
			var python = child.spawn('python', [ __dirname + '/database/vcf_gt_count.py', gl])
			var chunk = ''

			python.stdout.on('data', function (data) {
				chunk += data
				fulfill(chunk)
			}) //close stdout
			python.stderr.on('data', function (data) {
				console.log('python err: ' + data)
				response.end('python error in allele counts!' + data)
			}) //close stderr
		})
	}
=======
	function vcf_allele_freqs(coordJSON) {
		return new Promise(function (resolve, reject) {
			var start = coordJSON["start"]
			var end = coordJSON["end"]
			var chrom = coordJSON["chrom"]

			var python = child.spawn('python', [__dirname + '/database/vcf_allele_freq.py', chrom, start, end])
			var chunk = ''

			python.stdout.on('data', function(data) {
				chunk += data
				console.log(chunk)
				resolve(chunk)
			}) // close std out
			//catch python error message:
			python.stderr.on('data', function(data) {
				console.log('python stderr: ' + data)
				response.end('python error! ' + data)
			}) //close stderr
		}) //close promise
	} //close vcf_allele_frequency function
>>>>>>> master

	queryByRegulator(showRegulator)
}) //close app.post

var template = 'Node app is running at localhost: {port~number}'
var txt = template.replace('{port~number}', app.get('port'))

app.listen(app.get('port'), function() {
    console.log(txt)
})


