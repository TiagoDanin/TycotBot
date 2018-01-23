from models.base import Base, engine, Session
from queries import make_query
from models.group import Group


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


def welcome_msg(group_id, text):
    group = make_query(Group, Group.group_id == group_id)
    group.welcome_msg = text


def commit_and_close():
    session.commit()
    session.close()
