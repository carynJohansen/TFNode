# This file is the master python script,
# that will run each of the parsers and populate the database.

###############################
#           Env               #

import models
import config
import gffProcessor
import sqlA_insert as insert
import vcf_parse

###############################
#           Main              #

if __name__ == "__main__":
	#parse the gff and populate the database
	print "Creating database\n"
	models.main()
	print "Load GFF into gene_model database\n"
	gffProcessor.main(config.GFF, config.CHROMOSOMES)
	print "Load the interaction network into database\n"
	insert.main()
	print "Populate the VCF tables"
	vcf_parse.main()