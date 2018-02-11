from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://usr:pass@localhost:5432/tycot')

# create a configured "Session" class
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
