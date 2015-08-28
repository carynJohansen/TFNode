###################
#       Env       #
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pandas.io import sql
import numpy as np
import pandas as pd
from StringIO import StringIO

import config

###################
#    SQL Engine   #

engine = create_engine('sqlite:///' + config.DATABASE)
connect = engine.connect().connection

#Base.metadata.bind = engine
#DBSession = sessionmaker(bind=engine)
#session = DBSession()

###################
#     Methods	  #

def parse_network(netfile):
	"""Open network file, read to memory"""
	with open(netfile, 'r') as f:
		contents = f.read()

	#This returns a pandas data frame, with 8 columns
	data = pd.DataFrame(np.genfromtxt(StringIO(contents), delimiter="\t", dtype=None,
		names = True))
	return data

def pop_tmp_interNetwork(network_full):
	"""fill the interaction network temprorary table"""
	network_full.to_sql(con=connect, name='interaction_network_tmp', if_exists='replace', index=True, index_label='id')

def pop_interNetwork():
	sql_st = '''SELECT tmp.id as int_id, gm.id as regulator, gm_target.id as target, tmp.prior as in_prior\
		FROM gene_model as gm\
		INNER JOIN interaction_network_tmp as tmp ON (tmp.regulator = gm.gene_locus)\
		INNER JOIN gene_model as gm_target ON (tmp.target = gm_target.gene_locus)\
		GROUP BY int_id'''

	#returns Nx3 pandas DataFrame:
	data = sql.read_sql(sql_st, con=connect)

	#populate the interaction_network table
	data.to_sql(con=connect, name='interaction_network', if_exists='replace', index=False)

def pop_interStats():
	sql_st = '''SELECT tmp.id as interaction_id, tmp.betasignsum as beta_sign_sum,\
		tmp.betanonzero as beta_non_zero, tmp.betamedian as beta_median,\
		tmp.varexpmedian as exp_var_median, tmp.varexpranksum as var_exp_ranksum\
		FROM interaction_network_tmp as tmp'''
	data = sql.read_sql(sql_st, con=engine)

	#populate the interaction_stats table using pandas.to_sql and the SQLAlchemy engine
	data.to_sql(con=engine, name='interaction_stats', if_exists='replace', index=False)

#def remove_tmp_tables():
#	#Need to figure out a way to remove the one temporary table... how do you do this??
#	#sql.read_sql('DROP TABLE interaction_network_tmp', con=connect)
#	#SQLAlchemy.sql.expression.delete('interaction_network_tmp')


###################
#      Main 	  #

def main():
	#Parse the network, return as a pandas DataFrame
	print "Parsing interaction network data\n"
	data = parse_network(config.NET)

	#create the temporary interaction network
	pop_tmp_interNetwork(data)

	#use the temporary interaction network to populate the interaction_network table
	print "Filling the interaction network table, 'interaction_network'\n"
	pop_interNetwork()

	#use the temporary interaction network to populate the interaction_stats table
	print "Filling interaction statistics table, 'interaction_stats'\n"
	pop_interStats()

	#remove the temporary table
	#remove_tmp_tables()

if __name__ == '__main__':
	main()
