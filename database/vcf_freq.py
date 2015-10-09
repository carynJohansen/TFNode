###############################
#           Env               #

from BCBio import GFF
from sqlalchemy import create_engine
from pandas.io import sql
import sys
import numpy as np
import pandas as pd
import json

#import config
import vcf

#to time the program:
import time

###############################
#         SQL Engine          #

#engine = create_engine('sqlite:///' + config.DATABASE)
#connect = engine.connect().connection
#print engine

###############################
#          Methods            #

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

def test_answers(chrom, start, end):
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
	vcf_reader = get_vcf_reader()

	position_array = []

	for record in vcf_reader.fetch(chrom, int(start), int(end)):
		position_array.append(record.POS)

	return position_array

def combine_arrays(position_array, sample_gt_array):
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
	all_count = []
	ref = 0
	alt = 0
	no_data = 0

	for i in allele_array:
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
		#reset variables
		ref = 0
		alt = 0
		no_data = 0

	return all_count

def gt_counter(gtDF):
	genotypes = []
	ref_hm = 0
	alt_hm = 0
	het = 0
	for i in gtDF.iterrows():
		record = {}
		#print idx
		for j in i[1]:
			if (j == '0/0'):
				ref_hm += 1
			elif (j == '1/1'):
				alt_hm += 1
			elif (j == '0/1' or j == '1/0'):
				het += 1
			record = {
				'position':i[0],
				'ref_hm' : ref_hm,
				'alt_hm' : alt_hm,
				'hets' : het
			}
		genotypes.append(record)
		#reset variables
		ref_hm = 0
		alt_hm = 0
		het = 0
	return genotypes
#def main():


###############################
#            Main             #

if __name__ == '__main__':
	file, chrom, start, end = sys.argv
	samples = get_samples()
	gt_dictionary = get_genotypes(chrom, start, end, samples)
	position_array = get_position_array(chrom, start, end)
	full_data = combine_arrays(position_array, gt_dictionary)
	#print full_data
	alleles = allele_lists(full_data)
	all_counts = allele_counter(alleles)
	print all_counts
	genotype_counts = gt_counter(full_data)
	print genotype_counts
	#print samples
	sys.stdout.flush()