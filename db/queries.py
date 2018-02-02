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


def filter_by_group_id(table, value):
    return session.query(table).filter_by(group_id=value).first()


def get_total_warns(username='', user_id=''):
    '''
    Get total warns from a spefic user. You can choose which parameter to use, for filter
    the user.
    user_id -- id of the user
    '''
    return session.query(User.total_warns).filter_by(user_id=user_id).first()[0]


def get_welcome_msg(group_id):
    return filter_by_group_id(Group.welcome_msg, group_id)[0]


def get_rules(group_id):
    return filter_by_group_id(Group.rules, group_id)[0]


def get_link(group_id):
    return filter_by_group_id(Group.link, group_id)[0]
