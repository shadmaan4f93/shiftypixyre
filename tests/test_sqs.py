import json
from unittest.mock import Mock, patch

import pytest

from lambdas.dal.sqs import save_shift, save_shifter, sqs
from tests.helpers import mock_dal_post

# Loads a mocked response from SQS
with open('testdata/sqs.json') as json_data:
    TEST_DATA = json.load(json_data)


class TestSQS:
    @patch('lambdas.utils.util.requests.post', side_effect=mock_dal_post)
    def test_sqs(self, mock_dal):
        print("======================== Test sqs function ==================")
        self.result = sqs(TEST_DATA["sqs_body"])
        assert self.result['statusCode'] == 200 and self.result['body'] == "Success"

    def test_shifter(self):
        print("======================== Test shifter save function ==================")
        self.result = save_shifter(TEST_DATA["shifter_data"])
        assert self.result['statusCode'] == 200 and self.result['body'] == "Success"

    def test_shift(self):
        print("======================== Test shift save ==================")
        self.result = save_shift(TEST_DATA["shift_data"])
        assert self.result['statusCode'] == 200 and self.result['body'] == "Success"
