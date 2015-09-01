###############################
#           Env               #
import sys
from BCBio import GFF
from sqlalchemy import create_engine
from pandas.io import sql
import numpy as np
import pandas as pd

import config

#to time the program:
import time

###############################
#         SQL Engine          #

engine = create_engine('sqlite:///' + config.DATABASE)
connect = engine.connect().connection
#print engine

###############################
#          Methods            #

def gff_to_DF(chromosome, gff):
	'''Open the given GFF file and parse the contents into a pandas DF'''
	print "Converting GFF to DF"
	#set the limiting information to filter the 
	# gff file
	limit_info = dict(
		gff_id = [chromosome],
		gff_type = ["gene"])

	#make the empty gff list to store the gff information
	gff_list = []

	#set the seqid, until I figure out how to extract this I will have to loop
	# over all the chromosomes.
	seqid = chromosome

	#open the gff file
	in_handle = open(gff)

	#use GFF from BCBio to parse through the GFF. It creates a SeqFeature object
	#	that you call information from. 'feature' is that object, and there is one feature per
	#	record in the GFF.
	#Note: this is probably inefficient. I'm testing that soon.
	for rec in GFF.parse(in_handle, limit_info=limit_info):
		for feature in rec.features:
			record = []
			record.append(feature.id)
			record.append(seqid)
			#record.append(feature.qualifiers['source'])
			record.append(str(feature.type))
			record.append(int(feature.location.start))
			record.append(int(feature.location.end))
			record.append(feature.strand)
			#record.append(str(feature.qualifiers))
			gff_list.append(record)
		
	in_handle.close() #close file connection

	numberOfRows = len(gff_list)

	gff_df = pd.DataFrame(index = np.arange(1,numberOfRows+1), columns=('gene_locus', 
		'seqid', 'type', 'start', 'end', 'strand'))

	for i in np.arange(1, numberOfRows+1):
		gff_df.loc[i] = gff_list[i-1]

	print "Whew, done\n"
	return gff_df

def DF_to_sql(gene_model_df):
	'''Use the pandas DF of the gene model to populate the gene_model table in the SQL'''
	print "populating the DQL"
	
	gene_model_df.to_sql(con=connect, name='gene_model', if_exists='replace', index=True, index_label='id') 
	print "Whew, done\n"

def main(gff, chromosomes):
	#make a list of panda DataFrames for each of the Chromosomes
	gffs = [ gff_to_DF(chrm, gff) for chrm in chromosomes ]

	#Concatinate this into one large DataFrame:
	all_gffs = pd.concat( gffs, ignore_index=True , keys=chromosomes) #ignore_index=True enables a index from 0 to n-1 for final DF
	
	#Load into the SQL database
	DF_to_sql(all_gffs)

###############################
#            Main             #

if __name__ == '__main__':
	start_time = time.time()
	print sys.executable
	print GFF.__file__
	gff = config.GFF
	chromosomes = config.CHROMOSOMES
	
	main(gff, chromosomes)

	print("--- %s seconds ---" % (time.time() - start_time))

