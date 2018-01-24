from .models.base import Session
from .models.user import User
from .models.group import Group

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
    '''
    Get total warns from a spefic user. You can choose which parameter to use, for filter 
    the user.
    username -- Name of the user
    user_id -- id of the user
    '''
    if username:
        return session.query(User.total_warns).filter_by(user_name=username).first()
    else:
        return session.query(User.total_warns).filter_by(user_id=user_id).first()


def get_welcome_msg(group_id):
    return session.query(Group.welcome_msg).filter_by(group_id=group_id).first()
