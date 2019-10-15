import json
import iso8601
from lambdas.utils.datetime import DateTimeDuration


with open('testdata/commontest.json') as json_data:
    TEST_DATA = json.load(json_data)


DATETIME = iso8601.parse_date(TEST_DATA["start_time"])


class Testdatetimes:
    def test_is_iso_formate(self):
        print("======================== Test is_iso_formate function ==================")
        self.response = DateTimeDuration.is_iso_formate(TEST_DATA["start_time"])
        assert self.response is True

    def test_get_datetime_obj(self):
        print("======================== Test get_datetime_obj function ==================")
        datetime_obj = DateTimeDuration.get_datetime_obj(TEST_DATA["start_time"])
        self.type_datetime = type(datetime_obj)
        assert self.type_datetime.__name__ == 'datetime'

    def test_get_datetime_iso_str(self):
        print("======================== Test get_datetime_iso_str function ==================")
        datetime_str = DateTimeDuration.get_datetime_iso_str(DATETIME)
        self.type_datetime = type(datetime_str)
        assert self.type_datetime.__name__ == 'str'

    def test_get_duration(self):
        print("======================== Test get_duration function ==================")
        self.response = DateTimeDuration.get_duration(TEST_DATA["start_time"], TEST_DATA["end_time"], "hour")
        assert self.response == 24
