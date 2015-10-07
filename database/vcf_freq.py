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
	f = open('checkfile.txt', 'r+')
	for record in vcf_reader.fetch(chrom, int(start), int(end)):
		f.write(str(record))
		for sample in record.samples:
			f.write(str(sample.sample))
			f.write(str(sample['GT']))
	f.close()

def get_position_array(chrom, start, end):
	vcf_reader = get_vcf_reader()

	position_array = []

	for record in vcf_reader.fetch(chrom, int(start), int(end)):
		position_array.append(record.POS)

	return position_array

def combine_arrays(position_array, sample_gt_array):
	df = pd.DataFrame(sample_gt_array, index=position_array)
	return df

#def main():


###############################
#            Main             #

if __name__ == '__main__':
	file, chrom, start, end = sys.argv
	samples = get_samples()
	gt_dictionary = get_genotypes(chrom, start, end, samples)
	position_array = get_position_array(chrom, start, end)
	full_data = combine_arrays(position_array, gt_dictionary)
	print full_dataw
	#print samples
	sys.stdout.flush()