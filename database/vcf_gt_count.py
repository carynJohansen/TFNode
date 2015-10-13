###############################
#           Env               #

from BCBio import GFF
from sqlalchemy import create_engine
from pandas.io import sql
from pandas import DataFrame
import sys
import numpy as np
import pandas as pd
import json

import config
import vcf

#to time the program:
import time

###############################
#         SQL Engine          #

engine = create_engine('sqlite://' + config.DATABASE)
connect = engine.connect()
print connect

###############################
#          Methods            #

def get_coordinates(locus):
	sql_query = "SELECT gm.start, gm.end, gm.seqid as chrom FROM gene_model as gm WHERE (gm.gene_locus = %s)" % locus
	toresolve = connect.execute(sql_query)
	coords = DataFrame(toresolve.fetchall())
	print coords
	return coords


def get_vcf_reader():
	return vcf.Reader(open('/Users/carynjohansen/Documents/NYUClasses/Purugganan_Lab/TFInteraction_db/data/rice_chr2_3.vcf.gz', 'r'))

def get_samples():
	"""create and return an array of sample names from the vcf"""
	vcf_reader = get_vcf_reader()
	samples_array = []
	record = vcf_reader.next()
	
	for sample in record.samples:
		samples_array.append(sample.sample)
	return samples_array

def get_genotypes(chrom, start, end, sampleArray):
	"""get the genotypes for each position for each sample"""
	vcf_reader = get_vcf_reader()

	gt_dict = {}
	for i in sampleArray:
		gt = []
		for record in vcf_reader.fetch(chrom, int(start), int(end)):
			for sample in record.samples:
				if (i == sample.sample):
					gt.append(sample['GT'])
					
		gt_dict[i] = gt
	#test_answers(chrom, start, end)
	return gt_dict

def get_position_array(chrom, start, end):
	"""return an array of variant positions from vcf between start and end, on chrom."""
	vcf_reader = get_vcf_reader()
	position_array = []
	for record in vcf_reader.fetch(chrom, int(start), int(end)):
		position_array.append(record.POS)
	return position_array

def combine_arrays(position_array, sample_gt_array):
	"""return a dataframe of the genotypes, with the position array as the DF index."""
	df = pd.DataFrame(sample_gt_array, index=position_array)
	df.to_csv("genotypes.csv")
	return df

def gt_counter(gtDF):
	"""return counts for each genotype at each position."""
	genotypes = []

	for i in gtDF.iterrows():
		ref_hm = 0
		alt_hm = 0
		het = 0
		no_data = 0
		record = {}
		#print idx
		for j in i[1]:
			if (j == '0/0'):
				ref_hm += 1
			elif (j == '1/1'):
				alt_hm += 1
			elif (j == '0/1' or j == '1/0'):
				het += 1
			elif (j == './.'):
				no_data += 1
			record = {
				'position': i[0],
				'ref_hm' : ref_hm,
				'alt_hm' : alt_hm,
				'hets' : het,
				'no_data' : no_data
			}
		genotypes.append(record)

	return genotypes

###############################
#            Main             #

def main(locus):
	coords = get_coordinates(locus)

#	samples = get_samples()
#	gt_dictionary = get_genotypes(chrom, start, end, samples)
#	position_array = get_position_array(chrom, start, end)
#	full_data = combine_arrays(position_array, gt_dictionary)
#	genotype_counts = gt_counter(full_data)
#	return genotype_counts

if __name__ == '__main__':
	file, locus = sys.argv
	genotype_counts = main(locus)
	print genotype_counts
	sys.stdout.flush()

