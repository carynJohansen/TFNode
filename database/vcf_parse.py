###############################
#           Env               #

from BCBio import GFF
from sqlalchemy import create_engine
from pandas.io import sql
import numpy as np
import pandas as pd

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

def VCF_INFO_to_DF(vcf_reader):
	'''The purpose of this is to insert the information for each record of the VCF into a VCF_information table'''
	#create array to hold information
	vcf_arr = []

	for record in vcf_reader:
		row = []
		row.append(record.CHROM)
		row.append(record.POS)
		row.append(record.ID)
		row.append(record.REF)
		row.append(record.ALT[0])

		if record.QUAL != 0:
			row.append(record.QUAL)
		else:
			row.append('.')

		row.append(record.FILTER)
		row.append(record.FORMAT)
		vcf_arr.append(row)

	numOfRows = len(vcf_arr)
	vcf_df = pd.DataFrame(index=np.arange(1, numOfRows+1), columns=('CHROM', 'POS', 'ID',
		'REF', 'ALT', 'QUAL', 'FILTER', 'FORMAT'))

	for i in np.arange(1, numOfRows+1):
		vcf_df.loc[i] = vcf_arr[i-1]

	return vcf_df

def VCF_sample_to_DF():
	samples_arr = []
	vcf_reader = vcf.Reader(open(config.VCF, "rb"))

	record = vcf_reader.next()

	for sample in record.samples:
		row = []
		row.append(sample['name'])
		row.append(sample['GT'])
		samples_arr.append(row)

	numOfRows = len(samples_arr)

	sample_df = pd.DataFrame(index=np.arange(1, numOfRows+1), columns=('Sample', 'GT'))

	for i in np.arange(1, numOfRows+1):
		sample_df.loc[i] = samples_arr[i-1]

	return sample_df

def pop_vcf_info(vcf_info_df):
	"""populate the vcf_info table"""
	vcf_info_df.to_sql(con=engine, name='vcf_information', if_exists='replace', index=True, index_label='id')

def pop_vcf_sample_info(vcf_sample):
	"""populate the vcf_sample_info table with the sample genotype information"""
	vcf_sample.to_sql(con=connect, name='vcf_sample_info', if_exists='replace', index=False)

def main():
	"""The main method, carries out all table population processes"""
	#open VCF with vcf.Reader
	vcf_reader = vcf.Reader(open(config.VCF, "rb"))
	vcf_info = VCF_INFO_to_DF(vcf_reader)
	print vcf_info
	pop_vcf_info(vcf_info)

###############################
#            Main             #

if __name__ == '__main__':
	start = time.time()
	#open VCF with vcf.Reader
	vcf_reader = vcf.Reader(open(config.VCF, "rb"))

	vcf_info = VCF_INFO_to_DF(vcf_reader)
	sample = VCF_sample_to_DF()

	print vcf_info
	print sample.shape

	pop_vcf_info(vcf_info)
	pop_vcf_sample_info(sample)

	print("--- %s seconds ---" % (time.time() - start))
		