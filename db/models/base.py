from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://usr:pass@localhost:5432/tycot')

# create a configured "Session" class
# https://stackoverflow.com/questions/3039567/sqlalchemy-detachedinstanceerror-with-regular-attribute-not-a-relation
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()

Base = declarative_base()
