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
		
		console.log("Query (regulator) is: " + reqGL)

		db.all(sql_query, reqGL, function(err, rows) {
			if (err) {
				console.log(err)
			} else {
				whenDone(rows, reqGL)
			} //close ifelse
		}) //close db.all
	}) // close serialize
} // close queryByRegulator