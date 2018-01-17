from models.base import Session

session = Session()


def make_query(table, query):
    '''
    Make a query to the database
    table -- table to query
    query -- should be like this example:
        User.name == 'kleber'
    '''
    result = session.query(table).filter(query).all()
    return result
