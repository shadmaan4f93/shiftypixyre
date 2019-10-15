from mongoengine import *


def openconnection(connection_key):
    try:
        # Initialize connection string.
        mongo_port = int(27017)
        connection_kwargs = {
            'username': "abhinav",
            'host': "cluster0-shard-00-00-x2dzy.mongodb.net",
            'password': "abhi1234",
            'port': mongo_port,
            'authentication_source': "admin"
        }
        # Get connection.
        connect(connection_key['sample_airbnb'], **connection_kwargs)
        # Get connection object.
        connection = get_connection()
        # Get database.
        database = get_db()
        print(database)
    except BaseException as exceptions:
       print(exceptions)

print(openconnection("dfsd"))

#mongodb://abhinav:abhi1234@cluster0-shard-00-00-x2dzy.mongodb.net:27017")