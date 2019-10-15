import json
from lambdas.utils.calculations import Calculations
from lambdas.config.orgConfig import ConfigLoaders


CAL_OBJ = Calculations()
PATTERN = ConfigLoaders.get_organizationsetting("11e91af3559132a6869d0242ac110003")
SCORE_PATTERN = PATTERN["scoring_structures"]


with open('testdata/calculation.json') as json_data:
    TEST_DATA = json.load(json_data)


class Testcalculations():
    """ This test class ensure that all calcuation function work expected.  """

    def test_hour_match(self):
        print("======================== Test hour_match function ==================")
        instance = TEST_DATA['hour_match']
        params = SCORE_PATTERN["hour_match"]
        expected = TEST_DATA['hour_match']['expected']
        self.result = CAL_OBJ.execute('hour_match', instance, params)
        assert self.result == expected

    def test_distance(self):
        print("======================== Test distance function ==================")
        instance = TEST_DATA['distance']
        params = SCORE_PATTERN["distance"]
        expected = TEST_DATA['distance']['expected']
        self.result = CAL_OBJ.execute('distance', instance, params)
        assert self.result == expected

    def test_pay_match(self):
        print("======================== Test pay_match function ==================")
        instance = TEST_DATA['pay_match']
        params = SCORE_PATTERN["pay_match"]
        expected = TEST_DATA['pay_match']['expected']
        self.result = CAL_OBJ.execute('pay_match', instance, params)
        assert self.result == expected

    def test_profile_score(self):
        print("======================== Test profile_score function ==================")
        instance = TEST_DATA['profile_score']
        params = SCORE_PATTERN["profile_score"]
        expected = TEST_DATA['profile_score']['expected']
        self.result = CAL_OBJ.execute('profile_score', instance, params)
        assert self.result == expected

    def test_flexibility(self):
        print("======================== Test flexibility function ==================")
        instance = TEST_DATA['flexibility']
        params = SCORE_PATTERN["flexibility"]
        expected = TEST_DATA['flexibility']['expected']
        self.result = CAL_OBJ.execute('flexibility', instance, params)
        assert self.result == expected

    def test_reliability(self):
        print("======================== Test reliability function ==================")
        instance = TEST_DATA['reliability']
        params = SCORE_PATTERN["reliability"]
        expected = TEST_DATA['reliability']['expected']
        self.result = CAL_OBJ.execute('reliability', instance, params)
        assert self.result == expected

    def test_convenience(self):
        print("======================== Test convenience function ==================")
        instance = TEST_DATA['convenience']
        params = SCORE_PATTERN["convenience"]
        expected = TEST_DATA['convenience']['expected']
        self.result = CAL_OBJ.execute('convenience', instance, params)
        assert self.result == expected
