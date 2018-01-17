from models.base import Session

session = Session()


def make_query(table, query):
    '''
    Generic method to query the database
    table -- table to query
    query -- should be like this example:
        User.name == 'kleber'
    '''
    result = session.query(table).filter(query).all()
    return result
