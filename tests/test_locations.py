import json
from lambdas.utils.location import Geolocation


with open('testdata/commontest.json') as json_data:
    TEST_DATA = json.load(json_data)


CORDINATES = TEST_DATA["cordinates"]
ADDRESS = TEST_DATA["address"]


class Testlocations:
    def test_get_address(self):
        """ This test function ensure that get_address function return address as string. """
        print("======================== Test get_address function ==================")
        self.result = Geolocation.get_address(CORDINATES)
        ADDRESS = self.result
        assert self.result == ADDRESS

    def test_get_lat_lng(self):
        print("======================== Test get_lat_lng function ==================")
        self.result = Geolocation.get_lat_lng(ADDRESS)
        assert self.result != []

    def test_distance(self):
        print("======================== Test distance function ==================")
        self.result = Geolocation.distance(CORDINATES, CORDINATES)
        assert self.result == 0.0
