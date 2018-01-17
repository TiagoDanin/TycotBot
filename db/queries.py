from models.base import Session
from models.user import User

session = Session()


def make_query(table, query):
    '''
    Generic method to query the database
    table -- table to query
    query -- should be like this example:
        User.name == 'kleber'
    '''
    return session.query(table).filter(query).all()


def get_total_warns(username='', user_id=''):
    if username:
        return session.query(User.total_warns).filter_by(user_name=username).first()
    else:
        return session.query(User.total_warns).filter_by(user_id=user_id).first()
