import pytest
from lambdas.db.connection import DbConnection
from lambdas.config.config import CONNECTION_KEY


class Testconnection:
    """ To test database connection. """
    def test_connect(self):
        print("======================== Test database connection ==================")
        self.response = DbConnection.openconnection(CONNECTION_KEY)
        assert self.response["statusCode"] == 200
