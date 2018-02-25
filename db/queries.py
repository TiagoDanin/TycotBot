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
    '''
    Query a user from the db specified by his id.
    Return a User object. 
    user_id -- id of user
    '''
    return make_query(User, User.user_id == user_id)


def filter_by_group_id(column, group_id):
    '''
    Make a query to the db and return the first result.
    column -- column to query
    group_id -- id of the group
    '''
    return session.query(column).filter_by(group_id=group_id).first()


def get_max_warns(group_id):
    '''
    Get the max warn from the group 
    group_id -- id of the group
    '''
    return filter_by_group_id(Group.max_warns, group_id)[0]


def get_welcome_msg(group_id):
    '''Return the welcome message of the group.
    group_id -- id of the group'''
    return filter_by_group_id(Group.welcome_msg, group_id)[0]


def get_rules(group_id):
    '''Return the rules of the group.
    group_id -- id of the group'''
    return filter_by_group_id(Group.rules, group_id)[0]


def get_link(group_id):
    '''Return the link of the group.
    group_id -- id of the group'''
    return filter_by_group_id(Group.link, group_id)[0]


def group_exist(group_id):
    '''Verify if the group is in the database.
    group_id -- id of the group'''
    if make_query(Group, Group.group_id == group_id):
        return True
    return False


def user_exist(group_id, user_id):
    '''
    Verify if the user is in the database.
    user_id -- id of the user
    group_id -- id of the group
    '''
    for user in make_query(Group, Group.group_id == group_id)[0].users:
        if user.user_id == user_id:
            return True
    return False
