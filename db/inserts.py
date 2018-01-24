from .models.base import Base, engine, Session
from .queries import make_query
from .models.group import Group


Base.metadata.create_all(engine)

session = Session()


def addto_db(table):
    '''
    Get a table and add to db
    '''
    session.add(table)


def addsto_db(tables):
    '''
    Get a list of tables and add to db
    '''
    for table in tables:
        session.add(table)


def _current_session_obj(o):
    '''
    SqlAlchemy stuff
    see: https://stackoverflow.com/questions/24291933/sqlalchemy-object-already-attached-to-session
    '''
    curr_session = session.object_session(o)
    curr_session.add(o)
    curr_session.commit()
    curr_session.close()


def set_welcome_msg(group_id, text):
    group = make_query(Group, Group.group_id == group_id)[0]
    group.welcome_msg = text
    _current_session_obj(group)


def commit_and_close():
    session.commit()
    session.close()
