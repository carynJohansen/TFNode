###############################
#           Env               #

from BCBio import GFF
from sqlalchemy import create_engine
from pandas.io import sql
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

engine = create_engine('sqlite:///' + config.DATABASE)
connect = engine.connect().connection
#print engine

###############################
#          Methods            #

def get_vcf_reader():
	return vcf.Reader(open('/Users/carynjohansen/Documents/NYUClasses/Purugganan_Lab/TFInteraction_db/data/rice_chr2_3.vcf.gz', 'r'))

def get_coordinates(locus):
	#print con
	sql_query = "SELECT gene_model.start, gene_model.end, gene_model.seqid as chrom \
		FROM gene_model WHERE (gene_model.gene_locus = '%s')" % locus
	coords = sql.read_sql(sql_query, con=engine)
	return coords

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

def test_answers(chrom, start, end):
	"""write vcf parse results to a file, in order to test various stages of the parsing."""
	vcf_reader = get_vcf_reader()
	f = open('checkfile2.txt', 'r+')
	for record in vcf_reader.fetch(chrom, int(start), int(end)):
		f.write(str(record))
		for sample in record.samples:
			if (sample['GT'] == 'None'):
				f.write(str(sample.sample))
				f.write(str('./.'))
			else:
				f.write(str(sample.sample))
				f.write(str(sample['GT']))
				f.write('\t')
		f.write('\n')
	f.close()

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

def allele_lists(gtDF):
	"""split the genotype allele dataframe, count the instances of 0's and 1's
	for each position"""
	#print type(gtDF)
	alleles = []
	for i in gtDF.iterrows():
		record = []
		idx = i[0]
		record.append(idx)
		#print idx
		for j in i[1]:
			record.append(j.split('/')[0])
			record.append(j.split('/')[1])
		alleles.append(record)
	return alleles

def allele_counter(allele_array):
	"""return an array containing the counts for each allele at each position."""
	all_count = []

	for i in allele_array:
		ref = 0
		alt = 0
		no_data = 0
		row = {}
		for j in i:
			if (j == i[0]):
				continue
			if (j == '0'):
				ref += 1
			elif (j == '1'):
				alt += 1
			elif (j == '.'):
				no_data += 1
		row = {
			'position' : i[0],
			'ref_count' : ref,
			'alt_count' : alt,
			'no_data_count' : no_data
		}
		all_count.append(row)
	return all_count

###############################
#            Main             #

def main(locus):
	coords = get_coordinates(locus)
	start = coords["start"][0]
	end = coords["end"][0]
	chrom = str(coords["chrom"][0])
	samples = get_samples()
	gt_dictionary = get_genotypes(chrom, start, end, samples)
	position_array = get_position_array(chrom, start, end)
	full_data = combine_arrays(position_array, gt_dictionary)
	#print full_data
	alleles = allele_lists(full_data)
	all_counts = allele_counter(alleles)
	return all_counts

if __name__ == '__main__':
	file, locus = sys.argv
	all_counts = main(locus)
	print all_counts
	sys.stdout.flush()