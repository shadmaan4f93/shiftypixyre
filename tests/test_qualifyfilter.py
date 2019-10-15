import json
from lambdas.utils.qualifyfilter import QualifyFilter


QUALIFY_OBJ = QualifyFilter()


with open('testdata/disqualify.json') as json_data:
    TEST_DATA = json.load(json_data)


class Testdisqualify():

    def test_shift_overlap(self):
        print("======================== Test shift_overlap function ==================")
        inputs = TEST_DATA['shift_overlap']['input']
        expected = TEST_DATA['shift_overlap']['expected']
        result = QUALIFY_OBJ.execute('shift_overlap', inputs)
        assert result == expected

    def test_day_overtime_risk(self):
        print("======================== Test day_overtime_risk function ==================")
        inputs = TEST_DATA['day_overtime_risk']['input']
        expected = TEST_DATA['day_overtime_risk']['expected']
        result = QUALIFY_OBJ.execute('day_overtime_risk', inputs)
        assert result == expected

    def test_week_overtime_risk(self):
        print("======================== Test week_overtime_risk function ==================")
        inputs = TEST_DATA['week_overtime_risk']['input']
        expected = TEST_DATA['week_overtime_risk']['expected']
        result = QUALIFY_OBJ.execute('week_overtime_risk', inputs)
        assert result == expected

    def test_flexibility_filter(self):
        print("======================== Test flexibility_filter function ==================")
        inputs = TEST_DATA['flexibility_filter']['input']
        expected = TEST_DATA['flexibility_filter']['expected']
        result = QUALIFY_OBJ.execute('flexibility_filter', inputs)
        assert result == expected

    def test_reliability_filter(self):
        print("======================== Test reliability_filter function ==================")
        inputs = TEST_DATA['reliability_filter']['input']
        expected = TEST_DATA['reliability_filter']['expected']
        result = QUALIFY_OBJ.execute('reliability_filter', inputs)
        assert result == expected

    def test_recommended_filter(self):
        print("======================== Test recommended_filter function ==================")
        inputs = TEST_DATA['recommended_filter']['input']
        expected = TEST_DATA['recommended_filter']['expected']
        result = QUALIFY_OBJ.execute('recommended_filter', inputs)
        assert result == expected

    def test_position_filter(self):
        print("======================== Test position_filter function ==================")
        inputs = TEST_DATA['position_filter']['input']
        expected = TEST_DATA['position_filter']['expected']
        result = QUALIFY_OBJ.execute('position_filter', inputs)
        assert result == expected

    def test_duration_difference(self):
        print("======================== Test duration_difference function ==================")
        inputs = TEST_DATA['duration_difference']['input']
        expected = TEST_DATA['duration_difference']['expected']
        result = QUALIFY_OBJ.execute('duration_difference', inputs)
        assert result == expected
