from sqlalchemy import *
import config

engine = create_engine('sqlite:///' + config.DATABASE)