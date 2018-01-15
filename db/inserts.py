from models.base import Base, engine, Session


Base.metadata.create_all(engine)

session = Session()


def addto_db(table):
    '''
    Get a table and add to db
    '''
    session.add(table)
