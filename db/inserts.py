from models.base import Base, engine, Session


Base.metadata.create_all(engine)

session = Session()


def addto_db(table):
    '''
    Get a table and add to db
    '''
    session.add(table)


def addsto_db(*tables):
    '''
    Get a list of tables and add to db
    '''
    for table in tables:
        session.add(table)
