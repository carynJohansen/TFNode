import sqlite3 as lite
import config

#Connect
try:
	con = lite.connect(config.DATABASE)
	cursor = con.cursor()
	cursor.execute('SELECT SQLITE_VERSION()')
	data = cursor.fetchone()
	print "SQLite Version: %s" % data
except lite.Error, e:
	print "Error %s: " % e.args[0]
	sys.exit(1)

#create tables
cursor.execute('CREATE TABLE IF NOT EXISTS gene_model( \
	id INT primary key, \
	gene_locus VARCHAR, \
	seqid VARCHAR,\
	source VARCHAR,\
	type VARCHAR,\
	start INT,\
	end INT,\
	score INT,\
	strand VARCHAR,\
	phase VARCHAR,\
	attributes VARCHAR)')

cursor.execute('CREATE TABLE if not exists interaction_network(\
	id INT primary key,\
	regulator INT,\
	target INT,\
	in_prior INT,\
	foreign key (regulator) references gene_model(id),\
	foreign key (target) references gene_model(id) )')

cursor.execute('CREATE TABLE if not exists interaction_stats (\
	id INT primary key,\
	beta_non_zero INT,\
	beta_sign_sum INT,\
	beta_median REAL,\
	var_exp_median REAL,\
	var_exp_ranksum INT,\
	foreign key (id)references interaction_network(id))')

cursor.execute('CREATE TABLE if not exists regulation_graphics(\
	id INT primary key,\
	regulator_id INT,\
	tf_activity VARCHAR,\
	tf_expression VARCHAR,\
	binding_motif VARCHAR,\
	foreign key (regulator_id) references gene_model(id))')

#cursor.execute('CREATE TABLE if not exists coding_region_alignment(\
#	id INT primary key,\
#	regulator_id INT,\
#	alignment_summary VARCHAR,\
#	foreign key (regulator_id) references gene_model(id))')

#cursor.execute('CREATE TABLE if not exists motif_alignment\
#	id INT primary key,\
#	regulator_id INT,\
#	target_gene INT,\
#	interaction_id INT,\
#	alignment_summary VARCHAR,\
#	foreign key (regulator_id) references gene_model(id),\
#	foreign key (target_gene) references gene_model(id),\
#	foreign key (interaction_id) references interaction_network(id))')

#Commit create statements
con.commit()

#Close connection
con.close()
