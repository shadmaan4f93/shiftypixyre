import json

import requests
from requests.exceptions import RequestException

from lambdas.config.config import logger
from lambdas.utils.datetime import DateTimeDuration
from lambdas.utils.location import Geolocation


class CalculatorInstanceBuilder:
    """ This class is use to get instance of each score function. """

    def execute(self, method, inputs, pattern):
        """ This function is used to call the other function acording to function name.

        Args:
            method (string): Method name to call method Example: "distance".
            inputs (dict): qualified Shifter data and vacated shifter, shift data as dictionary.
            pattern  (list): Score pattern.

        Return:
            Instance: The return value. """
        try:
            method = getattr(self, method, lambda: 'Invalid')
            return method(inputs, pattern)
        except BaseException:
            return 'Invalid'

    @staticmethod
    def hour_match(inputs, pattern):
        """ This function is used to create instance for hour match score count function.

        Args:
            inputs (dict): Qualified shifter data and vacated shift, shifter data as dictionary.
            pattern  (list): Score pattern.

        Return:
            dict: The instance for calculate hour match score. """

        try:
            shifter_data = inputs["qualified_shifter"]["confirmedshifthours"]
            vacated_data = inputs["vacated_params"]
            shifter_hour_list = []
            for data in shifter_data:
                status = DateTimeDuration.is_date_match(data, vacated_data, "date")
                if status is True:
                    shifter_hour_list = DateTimeDuration.get_hour_list(data["starttime"], data["endtime"])
            vacated_hour_list = DateTimeDuration.get_hour_list(vacated_data["startTime"], vacated_data["endTime"])
            instance = {
                "hour_match": {
                    "input": {
                        "shifter_available_hour": shifter_hour_list,
                        "vacated_shifter_hour": vacated_hour_list
                    },
                    "pattern": pattern
                }
            }
            return instance
        except BaseException:
            return None

    @staticmethod
    def distance(inputs, pattern):
        """ This function is used to create instance for distance score count function.

        Args:
            inputs (dict): Qualified shifter data and vacated shifter data as dictionary.
            pattern  (list): Score pattern.

        Return:
            dict: The instance for calculate distance score. """

        try:
            shifter_data = inputs["qualified_shifter"]
            vacated_data = inputs["vacated_params"]
            source = {
                "longitude": vacated_data["location"][0],
                "latitude": vacated_data["location"][1]
            }
            destination = {
                "longitude": shifter_data["location"][0],
                "latitude": shifter_data["location"][1]
            }
            distances = Geolocation.distance(source, destination)
            instance = {
                "distance": {
                    "input": {
                        "distance": distances
                    },
                    "pattern": pattern
                }
            }
            return instance
        except BaseException:
            return None

    @staticmethod
    def pay_match(inputs, pattern):
        """ This function is used to create instance for pay match score function.

        Args:
            inputs (dict): Qualified shifter data and vacated shifter, shift data as dictionary.
            pattern  (list): Score pattern.

        Return:
            dict: The instance for calculate pay match score. """

        try:
            shifter_data = inputs["qualified_shifter"]
            vacated_data = inputs["vacated_params"]
            vacated_pay_rate = vacated_data["rate"]
            shifter_pay_rate = 0
            pay_type = None
            vacated_date = DateTimeDuration.get_datetime_obj(vacated_data["startTime"])
            vacated_day = vacated_date.weekday()
            for data in shifter_data["shifteravailability"]:
                if data["day"] == vacated_day:
                    shifter_pay_rate = data["minimumsalary"]
                    pay_type = data["minimumsalarytype"]
            instance = {
                "pay_match": {
                    "input": {
                        "shifter_pref_pay": vacated_pay_rate,
                        "vacated_shift_pay": shifter_pay_rate,
                        "pay_type": pay_type
                    },
                    "pattern": pattern
                }
            }
            return instance
        except BaseException:
            return None

    @staticmethod
    def profile_score(inputs, pattern):
        """ This function is used to create instance for profile score function.

        Args:
            inputs (dict): Qualified shifter data and vacated shifter, shift data as dictionary.
            pattern  (list): Score pattern.

        Return:
            dict: The instance for calculate profile score value. """

        try:
            shifter_data = inputs["qualified_shifter"]
            shifter_score = shifter_data["rating"]
            instance = {
                "profile_score": {
                    "input": {
                        "shifter_score": shifter_score
                    },
                    "pattern": pattern
                }
            }
            return instance
        except BaseException:
            return None

    @staticmethod
    def flexibility(inputs, pattern):
        """ This function is used to create instance for felxibility score function.

        Args:
            inputs (dict): Qualified shifter data and vacated shifter, shift data as dictionary.
            pattern  (list): Score pattern.

        Return:
            dict: The instance for calculate flexibility score value. """

        try:
            shifter_data = inputs["qualified_shifter"]
            invited_count = shifter_data["invitedcount"]
            accepted_count = shifter_data["acceptedcount"]
            instance = {
                "flexibility": {
                    "input": {
                        "times_invited": invited_count,
                        "times_accepted": accepted_count
                    },
                    "pattern": pattern
                }
            }
            return instance
        except BaseException:
            return None

    @staticmethod
    def reliability(inputs, pattern):
        """ This function is used to create instance for reliability score function.

        Args:
            inputs (dict): Qualified shifter data and vacated shifter, shift data as dictionary.
            pattern  (list): Score pattern.

        Return:
            dict: The instance for calculate reliability score value. """

        try:
            shifter_data = inputs["qualified_shifter"]
            noshow_count = shifter_data["noshowcount"]
            instance = {
                "reliability": {
                    "input": {
                        "shifetr_no_show": noshow_count
                    },
                    "pattern": pattern
                }
            }
            return instance
        except BaseException:
            return None

    @staticmethod
    def convenience(inputs, pattern):
        """ This function is used to create instance for convenience score function.

        Args:
            inputs (dict): Qualified shifter data and vacated shifter, shift data as dictionary.
            pattern  (list): Score pattern.

        Return:
            dict: The instance for calculate convenience score value. """

        try:
            shifter_data = inputs["qualified_shifter"]["confirmedshifthours"][0]
            vacated_data = inputs["vacated_params"]
            shifter_hour_list = DateTimeDuration.get_hour_list(shifter_data["starttime"], shifter_data["endtime"])
            vacated_hour_list = DateTimeDuration.get_hour_list(vacated_data["startTime"], vacated_data["endTime"])
            instance = {
                "convenience": {
                    "input": {
                        "shifter_branch": shifter_data["existingshifterjpid"],
                        "Vacated_shift_branch": vacated_data["jobProviderId"],
                        "shifter_shift_hour": shifter_hour_list,
                        "vacated_shift_hours": vacated_hour_list
                    },
                    "pattern": pattern
                }
            }
            return instance
        except BaseException:
            return None

# =================================================================================================


class DisqualifyInstanceBuilder:
    """ This class is use to get instance of each disqualify function. """

    def execute(self, method, inputs, discualify_params):
        """ This function is used to call the other function acording to function name.

        Args:
            method (string): Method name to call method Example: "distance".
            inputs (dict): Shifter data and vacated shifter data as dictionary.
            pattern  (list): Score pattern.

        Return:
            Instance: The return value. """
        try:
            method = getattr(self, method, lambda: 'Invalid')
            return method(inputs, discualify_params)
        except BaseException:
            return 'Invalid'

    @staticmethod
    def shift_overlap(inputs, discualify_params):
        """ This function is used to create instance for shift overlap filter function.

        Args:
            inputs (dict): Shifter data and vacated shift data as dictionary.
            discualify_params  (list): Disqualify pattern.

        Return:
            Instance: The return value. """
        try:
            shifter_shift_data = inputs["shifter"]["confirmedshifthours"]
            vacated_data = inputs["vacated_params"]
            vacated_hour_list = DateTimeDuration.get_hour_list(vacated_data["startTime"], vacated_data["endTime"])
            shifter_hour_list = []
            for data in shifter_shift_data:
                status = DateTimeDuration.is_date_match(data, vacated_data, "date")
                if status is True:
                    shifter_hour_list = DateTimeDuration.get_hour_list(
                        data["starttime"],
                        data["endtime"]
                    )
            instance = {
                "shift_overlap": {
                    "shifter_hour_list": shifter_hour_list,
                    "vacated_hour_list": vacated_hour_list,
                    "disqualify_params": discualify_params
                }
            }
            return instance
        except BaseException:
            return None

    @staticmethod
    def day_overtime_risk(inputs, discualify_params):
        """ This function is used to create instance for shift overtime risk filter function.

        Args:
            inputs (dict): Shifter data and vacated shift data as dictionary.
            discualify_params  (list): Disqualify pattern.

        Return:
            Instance: The return value. """
        try:
            shifter_shift_data = inputs["shifter"]["confirmedshifthours"]
            vacated_data = inputs["vacated_params"]
            vacated_hour = DateTimeDuration.get_duration(vacated_data["startTime"], vacated_data["endTime"], "hour")
            shifter_day_hour = 0
            for data in shifter_shift_data:
                status = DateTimeDuration.is_date_match(data, vacated_data, "date")
                if status is True:
                    day_hour = DateTimeDuration.get_duration(data["starttime"], data["endtime"], "hour")
                    shifter_day_hour = shifter_day_hour + day_hour
            instance = {
                "day_overtime_risk": {
                    "shifter_day_hour": shifter_day_hour,
                    "vacated_hour": vacated_hour,
                    "disqualify_params": discualify_params
                }
            }
            return instance
        except BaseException:
            return None

    @staticmethod
    def week_overtime_risk(inputs, discualify_params):
        """ This function is used to create instance for shift week overtime risk filter function.

        Args:
            inputs (dict): Shifter data and vacated shift data as dictionary.
            discualify_params  (list): Disqualify pattern.

        Return:
            Instance: The return value. """
        try:
            shifter_shift_data = inputs["shifter"]["confirmedshifthours"]
            vacated_data = inputs["vacated_params"]
            vacated_duration = DateTimeDuration.get_duration(
                vacated_data["startTime"],
                vacated_data["endTime"],
                "hour"
            )
            shifter_week_hour = 0
            for data in shifter_shift_data:
                status = DateTimeDuration.is_date_match(data, vacated_data, "week")
                if status is True:
                    duration = DateTimeDuration.get_duration(data["starttime"], data["endtime"], "hour")
                    shifter_week_hour = shifter_week_hour + duration
            instance = {
                "week_overtime_risk": {
                    "shifter_week_hour": shifter_week_hour,
                    "vacated_hour": vacated_duration,
                    "disqualify_params": discualify_params
                }
            }
            return instance
        except BaseException:
            return None

    @staticmethod
    def flexibility_filter(inputs, discualify_params):
        """ This function is used to create instance for shifter flexibility filter function.

        Args:
            inputs (dict): Shifter data and vacated shift data as dictionary.
            discualify_params  (list): Disqualify pattern.

        Return:
            Instance: The return value. """
        try:
            invited_count = inputs["shifter"]["invitedcount"]
            accepted_count = inputs["shifter"]["acceptedcount"]
            instance = {
                "flexibility_filter": {
                    "invitedcount": invited_count,
                    "acceptedcount": accepted_count,
                    "invited_range": discualify_params["invited_range"],
                    "accepted_range": discualify_params["accepted_range"]
                }
            }
            return instance
        except BaseException:
            return None

    @staticmethod
    def reliability_filter(inputs, discualify_params):
        """ This function is used to create instance for shifter flexibility filter function.

        Args:
            inputs (dict): Shifter data and vacated shift data as dictionary.
            discualify_params  (list): Disqualify pattern.

        Return:
            Instance: The return value. """
        try:
            noshow_count = inputs["shifter"]["noshowcount"]
            instance = {
                "reliability_filter": {
                    "noshowcount": noshow_count,
                    "noshow_range": discualify_params["noshow_range"]
                }
            }
            return instance
        except BaseException:
            return None

    @staticmethod
    def recommended_filter(inputs, discualify_params):
        """ This function is used to create instance for shifter flexibility filter function.

        Args:
            inputs (dict): Shifter data and vacated shift data as dictionary.
            discualify_params  (list): Disqualify pattern.

        Return:
            Instance: The return value. """
        try:
            recommended_count = inputs["shifter"]["recomendationcount"]
            invited_count = inputs["shifter"]["invitedcount"]
            instance = {
                "recommended_filter": {
                    "recommendedcount": recommended_count,
                    "invitedcount": invited_count,
                    "recommended_range": discualify_params["recommended_range"],
                    "invited_range": discualify_params["invited_range"]
                }
            }
            return instance
        except BaseException:
            return None

    @staticmethod
    def position_filter(inputs, discualify_params):
        """ This function is used to create instance for shifter flexibility filter function.

        Args:
            inputs (dict): Shifter data and vacated shift data as dictionary.
     >       discualify_params  (list): Disqualify pattern.

        Return:
            Instance: The return value. """
        try:
            completed_position_ids = inputs["shifter"]["vacatedshiftposition"]
            vacated_positionid = inputs["vacated_params"]["positionId"]
            completed_position_count = 0
            for positionid in completed_position_ids:
                if positionid["positionid"] == vacated_positionid:
                    completed_position_count = completed_position_count + 1
            instance = {
                "position_filter": {
                    "completed_position_count": completed_position_count,
                    "completed_position_range": discualify_params["completed_position_range"],
                }
            }
            return instance
        except BaseException:
            return None

    @staticmethod
    def duration_difference(inputs, discualify_params):
        """ This function is used to create instance for shifter flexibility filter function.

        Args:
            inputs (dict): Shifter data and vacated shift data as dictionary.
            discualify_params  (list): Disqualify pattern.

        Return:
            Instance: The return value. """
        try:
            shifter_shift_data = inputs["shifter"]["confirmedshifthours"]
            vacated_data = inputs["vacated_params"]
            duration_difference_list = []
            for data in shifter_shift_data:
                status = DateTimeDuration.is_date_match(data, vacated_data, "date")
                if status is True:
                    shifter_start_to_shift_end = DateTimeDuration.get_duration(
                        data["starttime"],
                        vacated_data["endTime"],
                        "hour"
                    )
                    shifter_end_to_shift_start = DateTimeDuration.get_duration(
                        data["endtime"],
                        vacated_data["startTime"],
                        "hour"
                    )
                    duration_difference_list.append(abs(shifter_start_to_shift_end))
                    duration_difference_list.append(abs(shifter_end_to_shift_start))
            instance = {
                "duration_difference": {
                    "duration_difference_list": duration_difference_list,
                    "duration_difference_range": discualify_params["duration_difference_range"]
                }
            }
            return instance
        except BaseException:
            return None


def get_api_data(url, body, token):
    """ This function use to get data from API.

    Args:
        url (string): required api url.
        body (dict): required request body

        Returns:
        json: The return value. """

    # Initialize return value.
    return_value = {
        "statusCode": None,
        "body": None
    }
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": token
        }
        response = requests.post(url, data=json.dumps(body), headers=headers)
        return_value["body"] = response
        return_value["statusCode"] = response.status_code
        if response.status_code == 200:
            logger.info("Successfully called %s with response code of %s", url, response.status_code)
        else:
            logger.error("Error calling %s, response code was: %s", url, response.status_code)
    except RequestException as ex:
        return_value["statusCode"] = 500
        return_value["body"] = str(RequestException)
        logger.error("Error calling %s, error was %s", url, str(ex))
    return return_value
