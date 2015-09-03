###############################
#           Env               #

from BCBio import GFF
from sqlalchemy import create_engine
from pandas.io import sql
from sys import argv
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

def get_vcf_reader():
	return vcf.Reader(open(config.VCF_COMP, "r"))

def get_record(chrom, position):
	vcf_reader = get_vcf_reader()
	position_record = []

	for record in vcf_reader:
		if record.CHROM == chrom and record.POS == int(position): 
			print "TRUE!"
			position_record = record
			break
	return position_record

def get_record_2(chrom, position):
	vcf_reader = get_vcf_reader()
	position_record = []

	for record in vcf_reader:
		while record.CHROM == chrom:
			if record.POS == position:
				position_record = record
				break
			break
	return position_record

def get_record_3(chrom, start, end):
	vcf_reader = vcf.Reader(open(config.VCF_COMP, "r"))
	position_record =[]
	for record in vcf_reader.fetch(chrom, start, end):
		row = []
		row.append(record.CHROM)
		row.append(record.POS)
		row.append(record.REF)
		row.append(record.ALT)
		position_record.append(row)
	return position_record

def get_samples():
	vcf_reader = get_vcf_reader()
	return vcf_reader.samples

###############################
#            Main             #

if __name__ == '__main__':
	file, POS, CHROM = argv
	start = time.time()
	#one = get_record(CHROM, POS)
	#print one
	print("just ifs: %s seconds" % (time.time() - start))
	start = time.time()
	#two = get_record_2(CHROM, POS)
	three = get_record_3(CHROM, 455511, 460716)
	print three
	print("two: %s seconds" % (time.time() - start))
