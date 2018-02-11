from .models.base import session
from .models.user import User
from .models.group import Group


def make_query(table, query):
    '''
    Generic method to query the database
    table -- table to query
    query -- should be like this example:
        User.name == 'kleber'
    '''
    return session.query(table).filter(query).all()


def get_user(user_id):
    return make_query(User, User.user_id == user_id)[0]


def filter_by_group_id(table, value):
    return session.query(table).filter_by(group_id=value).first()


def get_max_warns(group_id):
    '''
    Get total warns from a spefic user. You can choose which parameter to use, for filter
    the user.
    group_id -- id of the user
    '''
    return filter_by_group_id(Group.max_warns, group_id)[0]


def get_welcome_msg(group_id):
    return filter_by_group_id(Group.welcome_msg, group_id)[0]


def get_rules(group_id):
    return filter_by_group_id(Group.rules, group_id)[0]


def get_link(group_id):
    return filter_by_group_id(Group.link, group_id)[0]


def chat_exist(group_id):
    if make_query(Group, Group.group_id == group_id):
        return True
    return False
