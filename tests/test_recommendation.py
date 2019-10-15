import json
import pytest
from lambdas.utils.location import Geolocation
from lambdas.re.recommendation import (
    get_shift_by_id,
    get_shifters_from_db,
    get_shifter_volatile_data
)

from tests.helpers import mock_dal_post
from unittest.mock import Mock, patch

with open('testdata/recommendation.json') as json_data:
    TEST_DATA = json.load(json_data)


# @pytest.mark.skip(reason="Skip for next changes")
class TestRecommendation:

    def test_get_shift_by_id(self):
        print("=============== Test get_shift_by_id function ==============")
        response = get_shift_by_id(TEST_DATA["vacated_params"]["shiftId"])
        self.result = 'False'
        if response["statusCode"] == 200:
            if response["body"][0]["shiftid"] == TEST_DATA["shiftid"]:
                self.result = "True"
        assert self.result == "True"

    def test_get_shifters_from_db(self):
        print("=============== Test get_shifters_from_db function ==============")
        response = get_shifters_from_db(TEST_DATA["vacated_params"], TEST_DATA["disquaifyparams"]["static_data_filter"])
        self.result = 'False'
        if response["statusCode"] == 200:
            self.result = 'True'
            for data in response["body"]:
                if data["shifterid"] == TEST_DATA["vacated_params"]["vacatedshifterid"]:
                    self.result = 'False'
                source = {
                    "longitude": TEST_DATA["vacated_params"]["location"][0],
                    "latitude": TEST_DATA["vacated_params"]["location"][1]
                }
                destination = {
                    "longitude": data["location"][0],
                    "latitude": data["location"][1]
                }
                distances = Geolocation.distance(source, destination)
                print(distances)
        assert self.result == 'True'

    @patch('lambdas.utils.util.requests.post', side_effect=mock_dal_post)
    def test_get_shifter_volatile_data(self, mock_dal):
        print("=============== Test get_shifter_volatile_data function ==============")
        response = get_shifter_volatile_data(TEST_DATA["shifters"], TEST_DATA["vacated_params"])
        self.status = "False"
        if response["statusCode"] == 200:
            self.status = "True"
        assert self.status == "True"
