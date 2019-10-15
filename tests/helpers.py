import json
from unittest import mock

# Load the mocked response from json file
with open("testdata/dal_get_shifter.json") as json_data:
    DAL_GET_SHIFTER_RESPONSE = json.load(json_data)


# Returns a mocked http response
def mock_dal_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = DAL_GET_SHIFTER_RESPONSE
            self.status_code = status_code

        def json(self):
            return self.json_data

    return MockResponse(None, 200)
