import json
from unittest.mock import Mock, patch

import pytest
from requests.exceptions import RequestException

from lambdas.config.config import DAL_URL
from lambdas.utils.util import get_api_data

with open('testdata/commontest.json') as json_data:
    TEST_DATA = json.load(json_data)


class Testutils():
    @patch('lambdas.utils.util.requests.post')
    def test_get_api_data(self, mock_dal):
        print("======================== Test get_api_data function ==================")
        mock_dal.return_value.status_code = 200
        self.result = get_api_data(DAL_URL["base_url"], TEST_DATA["shifter_api_params"], DAL_URL["token"])
        assert self.result["statusCode"] == 200

    @patch("lambdas.utils.util.logger")
    @patch('lambdas.utils.util.requests.post')
    def test_get_api_logging_on_success(self, mock_dal, mock_logger):
        print("======================== Test get_api_data function logs info ==================")
        mock_dal.return_value.status_code = 200
        self.result = get_api_data(DAL_URL["base_url"], TEST_DATA["shifter_api_params"], DAL_URL["token"])
        mock_logger.info.assert_called_with("Successfully called %s with response code of %s", DAL_URL["base_url"], 200)

    @patch('lambdas.utils.util.requests.post')
    def test_get_api_data_handles_non_200(self, mock_dal):
        print("======================== Test get_api_data function handles 401/non 200 responses ==================")
        mock_dal.return_value.status_code = 401
        self.result = get_api_data(None, None, None)
        assert self.result["statusCode"] == 401

    @patch('lambdas.utils.util.requests.post')
    def test_get_api_data_handles_error(self, mock_dal):
        print("======================== Test get_api_data function handles error ==================")
        mock_dal.return_value.status_code = 500
        self.result = get_api_data(None, None, None)
        assert self.result["statusCode"] == 500

    @patch("lambdas.utils.util.logger")
    @patch('lambdas.utils.util.requests.post')
    def test_get_api_logging_on_error(self, mock_dal, mock_logger):
        print("======================== Test get_api_data function logs errors ==================")
        mock_dal.return_value.status_code = 500
        self.result = get_api_data(None, None, None)
        mock_logger.error.assert_called_with("Error calling %s, response code was: %s", None, 500)

    def test_get_api_handles_exception(self):
        print("======================== Test get_api_data function handles exception ==================")
        self.result = get_api_data(None, None, None)
        assert self.result["statusCode"] == 500

    @patch("lambdas.utils.util.logger")
    def test_get_api_logs_exception(self, mock_logger):
        print("======================== Test get_api_data function logs exception ==================")
        self.result = get_api_data(None, None, None)
        mock_logger.error.assert_called()
