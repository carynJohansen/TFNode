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

def VCF_INFO_to_DF():
	'''The purpose of this is to insert the information for each record of the VCF into a VCF_information table'''
	print("In VCF_into_to_DF!")
	vcf_reader = get_vcf_reader()
	#create array to hold information
	vcf_arr = []

	for record in vcf_reader:
		row = []
		row.append(record.CHROM)
		row.append(record.POS)
		row.append(record.ID)
		row.append(record.REF)
		row.append(record.ALT[0]) #this is a string
		if record.QUAL != 0:
			row.append(record.QUAL)
		else:
			row.append('.')

		row.append(record.FILTER)
		row.append(record.FORMAT)
		#print("Row:")
		#print(row)
		vcf_arr.append(row)

	numOfRows = len(vcf_arr)

	vcf_df = pd.DataFrame(index=np.arange(1, numOfRows+1), columns=('CHROM', 'POS', 'ID_type',
		'REF', 'ALT', 'QUAL', 'FILTER', 'FORMAT'))

	for i in np.arange(1, numOfRows+1):
		vcf_df.loc[i] = vcf_arr[i-1]

	print("Whew! done. \n")
	return vcf_df

def samples_to_table():
	print("In samples_to_table")
	vcf_reader = get_vcf_reader()
	samples_arr = []
	record = vcf_reader.next()
	
	for sample in record.samples:
		samples_arr.append(sample['name'])

	numOfRows=len(samples_arr)
	columns = ['sample_names']
	sample_df = pd.DataFrame(index=np.arange(1, numOfRows+1), columns=columns)

	for i in np.arange(1, numOfRows+1):
		sample_df.loc[i] = samples_arr[i-1]
	sample_df.to_sql(con=engine, name='samples', if_exists='replace', index=True, index_label='id')

def VCF_sample_to_DF():
	print("In VCF_sample_to_DF!")
	vcf_reader = vcf.Reader(open(config.VCF, "rb"))
	samples_table = get_samples()
	samples_table = samples_table.set_index(['sample_names'])
	samples_arr = []

	for record in vcf_reader:
		vcf_id = get_vcf_id(record.POS)
		for sample in record.samples:
			row = []
			row.append(int(vcf_id.loc[0]))
			row.append(int(samples_table.loc[sample['name']]))
			row.append(sample['GT'])
			samples_arr.append(row)
		vcf_row_counter += 1

	numOfRows = len(samples_arr)
	sample_df = pd.DataFrame(index=np.arange(1, numOfRows+1), columns=('vcf_id', 'Sample_id', 'GT'))

	for i in np.arange(1, numOfRows+1):
		sample_df.loc[i] = samples_arr[i-1]

	print("Whew! done. \n")
	return sample_df

def pop_vcf_info(vcf_info_df):
	"""populate the vcf_info table"""
	print("In pop_vcf_info")
	vcf_info_df.to_sql(con=engine, name='vcf_information', if_exists='replace', index=True, index_label='id')
	print("Whew! done")

def pop_vcf_sample_info(vcf_sample):
	"""populate the vcf_sample_info table with the sample genotype information"""
	print("In pop vcf_sample_info")
	vcf_sample.to_sql(con=connect, name='vcf_sample_info', if_exists='replace', index=False)
	print("Whew! done.")

######
#Gets

def get_samples():
	sql_stmt = "SELECT * from samples"
	samples = sql.read_sql(sql_stmt, con=connect)
	return samples

def get_vcf_id(position):
	sql_stmt = "SELECT id from vcf_information where POS=%s" % position
	vcf = sql.read_sql(sql_stmt, con=connect)
	return vcf

def get_vcf_reader():
	return vcf.Reader(open(config.VCF, "rb"))

###############################
#            Main             #

def main():
	"""The main method, carries out all table population processes"""
	start = time.time()
	vcf_info = VCF_INFO_to_DF()
	pop_vcf_info(vcf_info)

	samples_to_table()

	sample = VCF_sample_to_DF()
	pop_vcf_sample_info(sample)
	print("--- %s seconds ---" % (time.time() - start))


if __name__ == '__main__':
	start = time.time()
	#open VCF with vcf.Reader
	vcf_reader = get_vcf_reader()

	vcf_info = VCF_INFO_to_DF(vcf_reader)
	pop_vcf_info(vcf_info)

	samples_to_table()

	sample = VCF_sample_to_DF()
	pop_vcf_sample_info(sample)

	print("--- %s seconds ---" % (time.time() - start))
		
