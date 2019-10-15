import json

from mongoengine import QuerySetManager

from lambdas.config.config import CONNECTION_KEY, DAL_URL, logger
from lambdas.config.orgConfig import ConfigLoaders
from lambdas.db.connection import DbConnection
from lambdas.schema.models import Shifters, Shifts
from lambdas.utils.calculations import Calculations
from lambdas.utils.qualifyfilter import QualifyFilter
from lambdas.utils.util import (CalculatorInstanceBuilder,
                                DisqualifyInstanceBuilder, get_api_data)

FILTER = QualifyFilter()
CALC = Calculations()
DISQUALIFY = QualifyFilter()

LOG_HEADER = "--------------------------- | Shifter ID: %s | ---------------------------"


def get_shift_by_id(shift_id):
    """ This function used to get shift by shift id.

    Args:
        shift_id (string): shift id as string.

    Returns:
        dict: (shift associated with given shift id) The return value. """
    # Initialize return value.
    return_value = {
        "statusCode": None,
        "message": None,
        "body": None
    }
    try:
        # Check if class Shifts has no objects member.
        if 'objects' not in dir(Shifts):
            # Assign objects member.
            Shifts.objects = QuerySetManager()
        # Initialize database connection
        response = DbConnection.openconnection(CONNECTION_KEY)
        if response["statusCode"] == 200:
            response = Shifts.objects(shiftid=shift_id).to_json(indent=0)
            shift_data = json.loads(response)
            if shift_data:
                logger.info("Get Shift data from database success.")
                return_value["statusCode"] = 200
                return_value["message"] = "Success"
                return_value["body"] = shift_data
            else:
                logger.info("Shift data associated with vacated shift not found!.")
                return_value["statusCode"] = 404
                return_value["message"] = "Shift data not found for vacated shift"
                return_value["body"] = []
        else:
            return_value = response
    except KeyError:
        message = str(KeyError)
        logger.info("Error found in get_shift_by_id function! Error: %s", message)
        return_value["statusCode"] = 500
        return_value["message"] = "Internal server error"
        return_value["body"] = []
    return return_value


def get_shifters_from_db(vacated_params, disqualify_params):
    """ This function used to get filtered shifters data from database.

    Args:
    vacated_params (dict): Vacated shift, shifter data.
    disqualify_params (dict): paramiters to filter data

    Returns:
    dict: The return value. """
    # Initialize return value.
    return_value = {
        "statusCode": None,
        "message": None,
        "body": None
    }
    try:
        # Check if class Shifters has no objects member.
        if 'objects' not in dir(Shifters):
            # Assign objects member.
            Shifters.objects = QuerySetManager()
        # Initialize database connection
        response = DbConnection.openconnection(CONNECTION_KEY)
        if response["statusCode"] == 200:
            # Get data from database
            result = Shifters.objects.get_shifters(vacated_params, disqualify_params).to_json(indent=0)
            shifters = json.loads(result)
            if shifters:
                logger.info("Get shifters data from database success.")
                return_value["statusCode"] = 200
                return_value["message"] = "Seccess"
                return_value["body"] = shifters
            else:
                logger.info("Shifters not found in database!")
                return_value["statusCode"] = 404
                return_value["message"] = "Shifters not found in database!"
                return_value["body"] = []
        else:
            return_value = response
    except BaseException as ex:
        logger.error("Error retrieving data from MongoDB. %s", repr(ex))
        return_value["statusCode"] = 500
        return_value["message"] = "Internal server error!"
        return_value["body"] = []
    return return_value


def get_shifter_volatile_data(shifters, vacated_params):
    """ This function is used to get shifters voatile data from dal api.

    Args:
    shifters (List): List of filtered shifter data.

    Returns:
    dict: The return value. """
    # Initialize return value.
    return_value = {
        "statusCode": None,
        "message": None,
        "body": {}
    }
    try:
        # Initialize request body for call dal api type: "qualify".
        shifter_ids_list = []
        for shifter in shifters:
            shifter_ids_list.append(shifter["shifterid"])
        shifter_ids = ", ".join(shifter_ids_list)
        request_body = {
            "ID": shifter_ids,
            "Type": "qualify",
            "VacatedShiftDate": vacated_params["startTime"]
        }
        result = get_api_data(DAL_URL['base_url'], request_body, DAL_URL["token"])
        # To check if dal api call success.
        if result["statusCode"] == 200:
            logger.info("DAL api called successfully for type qualify.")
            data = result["body"].json()
            # To check data found.
            if data["data"]:
                logger.info("Shifters volatile data get success.")
                return_value["statusCode"] = 200
                return_value["message"] = "Success"
                return_value["body"] = data["data"]
            else:
                logger.error("Shifters volatile data not found!")
                return_value["statusCode"] = data['status']
                return_value["message"] = "Shifters volatile data not found!"
                return_value["body"] = []
        else:
            logger.error("Error calling DAL http response was: %s", result["statusCode"])
            return_value["statusCode"] = result["statusCode"]
            return_value["message"] = "Internal server error!"
            return_value["body"] = []
    except BaseException as exceptions:
        message = str(exceptions)
        logger.error("Error while gatting shifters volatile data %s", message)
        return_value["statusCode"] = 500
        return_value["message"] = "Internal server error!"
        return_value["body"] = []
    return return_value


def get_disqualify_status(disqualify_instances):
    """ This function used to perform disqualify filter and return status.

    Args:
    disqualify_instances (List): list of all filter function and associated params.

    Returns:
    List: The status of disqualify filter. """
    # Initialize qualify shifter
    disqualify_status = []
    try:
        for method, inputs in disqualify_instances.items():
            status = FILTER.execute(method, inputs)
            logger.debug("QualityFilter %s returned status of: %s", method, status)
            disqualify_status.append(status)
        return disqualify_status
    except BaseException as exceptions:
        message = str(exceptions)
        logger.error("Error while getting disqualify status: %s", message)
        return None


def get_combined_shifter(shifter_from_db, shifter_volatile_data):
    """ This function used to merge shifter_from_db and shifter_volatile_data.

    Args:
    shifter_from_db (dict): shifter data from database.
    shifter_volatile_data (dict): shifter volatile data

    Returns:
    dict: The return value. """

    # Initialize return value.
    return_value = {
        "statusCode": None,
        "message": None,
        "body": None
    }
    try:
        shifters_data = []
        if shifter_from_db["statusCode"] == 200 and shifter_volatile_data["statusCode"] == 200:
            for shifter in shifter_from_db["body"]:
                for additional_info in shifter_volatile_data['body']:
                    if additional_info['shifterid'] == shifter['shifterid']:
                        shifter.update(additional_info)
                        shifters_data.append(shifter)
            return_value["statusCode"] = 200
            return_value["message"] = "success"
            return_value["body"] = shifters_data
        else:
            return_value["statusCode"] = 404
            return_value["message"] = "shifter data not found"
            return_value["body"] = []
    except BaseException as exceptions:
        message = str(exceptions)
        return_value["statusCode"] = 500
        return_value["message"] = message
        return_value["body"] = []
    return return_value


def get_qualified_shifter(vacated_params, patterns):
    """ This function used to get qualified shifter.

    Args:
    vacated_params (dict): vacated shifter, shift data.

    Returns:
    dict: The return value. """

    # Initialize return value.
    return_value = {
        "statusCode": None,
        "message": None,
        "body": None
    }
    # Initialize array to store list of shifter with volatile data.
    shifters_data = []
    try:
        # To get filtered shifter from database.
        shifter_from_db = get_shifters_from_db(vacated_params, patterns["static_data_filter"])
        shifter_volatile_data = get_shifter_volatile_data(shifter_from_db["body"], vacated_params)
        shifters_data = get_combined_shifter(shifter_from_db, shifter_volatile_data)
        if shifters_data["statusCode"] == 200:
            qualified_shifter = []
            instance_builder = DisqualifyInstanceBuilder()
            logger.info("Getting qualified shifter for shiftId: %s and positionId: %s",
                        vacated_params["shiftId"], vacated_params["positionId"])
            for data in shifters_data["body"]:
                logger.info(LOG_HEADER, data["shifterid"])
                instances = {}
                inputs = {
                    "shifter": data,
                    "vacated_params": vacated_params
                }
                for method, pattern in patterns["volatile_data_filter"].items():
                    instance = instance_builder.execute(method, inputs, pattern)
                    if instance and instance != "Invalid":
                        instances.update(instance)
                filter_status = get_disqualify_status(instances)
                if "disqualified" not in filter_status:
                    instances.clear()
                    filter_status.clear()
                    qualified_shifter.append(data)
            if qualified_shifter:
                return_value["statusCode"] = 200
                return_value["message"] = "Success"
                return_value["body"] = qualified_shifter
                logger.info("Shifter is qualified")
            else:
                return_value["statusCode"] = 404
                return_value["message"] = "No qualified shifters found for this shift"
                return_value["body"] = []
                logger.info("Shifter was not qualified for the vacated shift")
        else:
            return_value = shifters_data
    except AttributeError as ex:
        return_value["statusCode"] = 500
        return_value["message"] = "Internal server error!"
        return_value["body"] = []
        logger.error("Error %s", repr(ex))
    return return_value


def get_shifter_score(instances):
    """ This function used to get shifter score.

    Args:
    instance (dict): shifter and vacated shifter required inputs to calculate score.
    qualified_params (dict): dictionary containing patter to get score.

    Returns:
    dict: (shift associated with given shift id) The return value. """

    shifter_score = 0
    try:
        for method_name, params in instances.items():
            score = CALC.execute(method_name, params['input'], params['pattern'])
            shifter_score = round(shifter_score + score, 2)
    except KeyError:
        shifter_score = 0
    return shifter_score


def get_top_shifters(shifter, top):
    """ This function used to get top number of shifter.

    Args:
    shifter (list): Qualified shifter list of dictionary with score.
    top (int) : params to get number of shifter with high score. Example: top = 3

    Returns:
    list: (shifter for recommend to cover vacated shift) The return value. """
    return_value = {
        "statusCode": None,
        "body": None
    }
    try:
        if shifter and top:
            # To sort the list of shifter in descending order
            soreted_shifter = sorted(shifter["body"], key=lambda k: k['score'], reverse=True)
            # To get top range shifter
            top_shifter = soreted_shifter[:top]
            shifters_id = []
            for data in top_shifter:
                shifters_id.append(data["shifterid"])
            return_value["statusCode"] = 200
            return_value["body"] = shifters_id
    except BaseException:
        return_value["statusCode"] = 200
        return_value["body"] = "Cant calculate top shifter"
    return return_value


def get_recommended_shifter(qualified_shifter, vacated_params, patterns):
    """ This function used to get recommended shifter.

    Args:
        qualified_shifter (dict): Qualified shifter data.
        vacated_params (dict): vacated shifter, shift data.
        patterns (dict): Organization pattern setting.

    Returns:
    dict: The return value. """

    # Initialize return value.
    return_value = {
        "statusCode": None,
        "message": None,
        "body": None
    }
    try:
        if qualified_shifter["statusCode"] == 200:
            for shifter in qualified_shifter["body"]:
                instance_obj = CalculatorInstanceBuilder()
                instances = {}
                inputs = {
                    "qualified_shifter": shifter,
                    "vacated_params": vacated_params
                }
                for method, pattern in patterns.items():
                    instance = instance_obj.execute(method, inputs, pattern)
                    if instance and instance != "Invalid":
                        instances.update(instance)
                score = get_shifter_score(instances)
                shifter["score"] = score
            recommended_shifter = get_top_shifters(qualified_shifter, 3)
            if recommended_shifter:
                return_value['statusCode'] = 200
                return_value["message"] = "Success"
                return_value["body"] = recommended_shifter["body"]
        else:
            return_value = qualified_shifter
    except KeyError:
        return_value['statusCode'] = 500
        return_value["message"] = "Internal server error!"
        return_value['body'] = []
    return return_value


def recommendations(vacated_params):
    """ This function used to get recommended shifter according to request params.

    Args:
    vacated_params (dict): vacated shift and shifter data.

    Returns:
    dict: (List of recommended shifter) The return value. """

    # Initialize return value
    return_value = {
        "statusCode": None,
        "message": None,
        "body": None
    }
    try:
        patterns = ConfigLoaders.get_organizationsetting(vacated_params["jobProviderId"])
        qualified_shifter = get_qualified_shifter(vacated_params, patterns["disqualify_structures"])
        return_value = get_recommended_shifter(qualified_shifter, vacated_params, patterns['scoring_structures'])
    except BaseException as ex:
        logger.error("Error in recommendation function. %s", str(ex))
        return_value['statusCode'] = 500
        return_value["message"] = "Internal server error!"
        return_value['body'] = []
    return return_value
