from mongoengine import connect
from mongoengine.connection import get_connection, get_db

from lambdas.config.config import logger


class DbConnection:
    """ This class is used to make connection with mongodb.

        Note: Class have static method to connect with database.
        Access Method: DbConnection.openconnection(connection_key) """

    @staticmethod
    def openconnection(connection_key):
        """ This function return connection object acording to connection params.

        Args:
        connection_key (dic): have following keys { username, host, password,
        port, authentication_source, db_name }.

        Returns:
        Object: The return value. """

        return_value = {
            "statusCode": None,
            "message": None,
            "body": None
        }
        try:
            # Initialize connection string.
            mongo_port = int(27017)
            try:
                mongo_port = int(connection_key["port"])
            except ValueError:
                logger.error("Mongo DB Port should be an integer. Provided value was: %s", connection_key["port"])
            connection_kwargs = {
                'username': connection_key['username'],
                'host': connection_key['host'],
                'password': connection_key['password'],
                'port': mongo_port,
                'authentication_source': connection_key['authSource']
            }
            # Get connection.
            connect(connection_key['db_name'], **connection_kwargs)
            # Get connection object.
            connection = get_connection()
            # Get database.
            database = get_db()
            if database.name == connection_key['db_name']:
                logger.info("Database connected successfully.")
                return_value["statusCode"] = 200
                return_value["message"] = "Success"
                return_value["body"] = connection
        except BaseException as exceptions:
            message = str(exceptions)
            logger.error("Database connection failed!: %s", message)
            return_value["statusCode"] = 500
            return_value["message"] = "Internal server error!"
            return_value["body"] = None
        return return_value
