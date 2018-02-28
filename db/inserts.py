from .models.base import Base, engine, session
from .queries import make_query
from .models.group import Group
from .models.user import User


def commit():
    '''Commit the changes to database'''
    session.commit()


def close():
    '''Close the session connection with the database'''
    session.close()


def commit_and_close():
    commit()
    close()


def remove_from_db(value):
    '''
    Remove some value from database
    value -- value to delete
    '''
    session.delete(value)
    commit_and_close()


def create_tables():
    '''
    see:
      http://docs.sqlalchemy.org/en/latest/core/metadata.html#creating-and-dropping-database-tables
    '''
    Base.metadata.create_all(engine)


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


def add_user(first_name, user_id, group_id):
    '''Add a user to the db
    first_name -- name of the user
    user_id -- id of the user
    group_id -- group id for the user to be added
    Return a user object
    '''
    user = User(first_name, user_id)
    group = make_query(Group, Group.group_id == group_id)[0]
    group.users = [user]
    commit_and_close()
    return user


def _current_session_obj(o):
    '''
    SqlAlchemy stuff
    see: https://stackoverflow.com/questions/24291933/sqlalchemy-object-already-attached-to-session
    '''
    curr_session = session.object_session(o)
    curr_session.add(o)
    curr_session.commit()
    curr_session.close()


def update_value(group_id, field, value):
    '''
    Update a column of the table Group filtered by its id
    group_id -- id of the group
    field -- column of the table Group to update
    value -- value to insert
    '''
    session.query(Group).filter(Group.group_id == group_id).update({field: value})


def set_welcome_msg(group_id, text):
    '''Set the welcome message of the group
    group_id -- id of the group
    text -- text to add to the db
    '''
    update_value(group_id, 'welcome_msg', text)
    commit_and_close()


def set_rules(group_id, text):
    update_value(group_id, 'rules', text)
    commit_and_close()


def set_chat_link(group_id, link):
    update_value(group_id, 'link', link)
    commit_and_close()


def set_max_warn(group_id, value):
    update_value(group_id, 'max_warns', value)
    commit_and_close()


def warn_user(group_id, user_id):
    for user in make_query(Group, Group.group_id == group_id)[0].users:
        if user.user_id == user_id:
            user.total_warns += 1
    commit_and_close()


def unwarn_user(group_id, user_id):
    for user in make_query(Group, Group.group_id == group_id)[0].users:
        if user.user_id == user_id:
            user.total_warns -= 1
    commit_and_close()
