function queryByTarget(whenDone) {
	db.serialize( function () {
		var tarGL = request.body.tar_gene_locus
		var sql_query = "SELECT gm2.gene_locus as regulator_locus \
		FROM interaction_network as inter \
		INNER JOIN gene_model as gm1 ON (inter.target = gm1.id) \
		INNER JOIN gene_model as gm2 ON (inter.regulator = gm2.id) \
		where (gm1.gene_locus=?)"

		console.log("Query (target) is: " + tarGL)

		db.all(sql_query, tarGL, function(err, rows) {
			if (err) {
				console.log(err) 
			} else {
				whenDone(rows, tarGL)
			} //close ifelse
		}) //close db.all
	}) //close db.serialize
} //close queryByTarget

function get_coordinates() {
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
				//console.log(rows)
				return rows
			}
		})//close db.all
	})//close db.serialize
}

function vcf_python(coordinates) {
	//coordinates is a JSON object with start and stop
	console.log(coordinates)
	//var start = json["start"]
	//var end = coordinates["end"]
	var python = child.spawn('python',[ __dirname + '/database/vcf_get.py', 6512743, 6518792, 'Chr3'])
	var chunk = ''
	
	python.stdout.on('data', function(data) {
		chunk += data
		json = JSON.stringify(chunk)
		json = json.replace(/(\n)/, "")
		response = JSON.parse(json)
		console.log(response)
	})
}