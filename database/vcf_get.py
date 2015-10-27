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

#engine = create_engine('sqlite:///' + config.DATABASE)
#connect = engine.connect().connection
#print engine

###############################
#          Methods            #

def get_vcf_reader():
	return vcf.Reader(open(config.VCF_COMP, "r"))

def get_records(chrom, start, end):
	vcf_reader = get_vcf_reader()
	position_record =[]
	for record in vcf_reader.fetch(chrom, int(start), int(end)):
		#print type(record.ALT)
		row = {
			"chromosome": record.CHROM,
			"position": record.POS,
			"reference": record.REF,
			"alternate": str(record.ALT[0])
		}
		position_record.append(row)
	positions_json = json.dumps(position_record)
	return positions_json

def get_samples():
	vcf_reader = get_vcf_reader()
	return vcf_reader.samples

def main(chrom, start, end):
	variant_info = get_records(chrom, start, end)
	return variant_info

###############################
#            Main             #

if __name__ == '__main__':
	file, chrom, start, end = sys.argv
	startTime = time.time()
	variant_info = main(chrom, start, end)
	print variant_info
	sys.stdout.flush()
	#print type(variant_info)
	#print("runtime: %s seconds" % (time.time() - startTime))
