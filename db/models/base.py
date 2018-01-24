from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://labatata101:#linuxfaustop1234@localhost:5432/tycot')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

Base = declarative_base()
