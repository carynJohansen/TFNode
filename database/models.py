from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

import config


engine = create_engine('sqlite:///' + config.DATABASE)

Base = declarative_base()

#from app import db
 
class Gene(Base):
    """the table to hold all the gene_model information"""
    __tablename__ = 'gene_model'
    id = Column(Integer, primary_key=True)
    gene_locus = Column(String(250), nullable=False)
    seqid = Column(String(250), nullable=False)
    #source = Column(String(250), nullable=False)
    type = Column(String(250), nullable=False)
    start = Column(Integer, nullable=False)
    end = Column(Integer, nullable=False)
    #score = Column(Integer, nullable=False)
    strand = Column(String(250), nullable=False)
    #phase = Column(String(250), nullable=False)
    #attributes=  Column(String(10000), nullable=False)

    def __init__(self, id, gene_locus):
        self.id = id
        self.gene_locus = gene_locus

    def __repr__(self):
        return 'Gene: %s' % (self.gene_locus)

    def get_gene_locus(self):
        try:
            return unicode(self.gene_locus)
        except GeneError:
            return "No gene of that locus name in the gene model"


class Interaction(Base):
    """The class for the table to hold the network interaction data"""
    __tablename__ = 'interaction_network'
    id = Column(Integer,primary_key=True)
    regulator = Column(Integer, ForeignKey('gene_model.id'))
    target = Column(Integer, ForeignKey('gene_model.id'))
    in_prior = Column(Integer)
    gene_model = relationship(Gene)

    def __init__(self, id, regulator, target, in_prior):
        self.id = id
        self.regulator = regulator
        self.target = target
        self.in_prior = in_prior

class Interaction_Stats(Base):
    """The class for the interaction statistics table."""
    __tablename__ = 'interaction_stats'
    id = Column(Integer, primary_key=True)
    id_interaction = Column(Integer)
    beta_sign_sum = Column(Integer)
    beta_non_zero = Column(Integer)
    beta_median = Column(Float)
    var_exp_median = Column(Float)
    var_exp_ranksum = Column(Integer)
   
    def __init__(self, id):
        self.id = id

class VCF_info(Base):
    """The class for the variant-specific information in the VCF"""
    __tablename__ = 'vcf_information'
    id = Column(Integer, primary_key=True)
    chrom = Column(String)
    position = Column(Integer)
    id_type = Column(String)
    ref = Column(String)
    alt = Column(String)
    qual = Column(String)
    filter = Column(String)
    format = Column(String)

    def __init__(self, id):
        self.id = id

class VCF_sample_info(Base):
    """The class for the sample-specific information stored in a VCF"""
    __tablename__ = 'vcf_sample_info'
    id = Column(Integer, primary_key=True)
    variant_id = Column(Integer, ForeignKey('vcf_information.id'))
    sample = Column(String)
    GT = Column(String)
    #Need to figure out how to do all the other keys for the VCF...
    vcf_information = relationship(VCF_info)

def database_init():
    Base.metadata.create_all(engine)

def main():
    database_init()

if __name__ == "__main__":
    main()   
