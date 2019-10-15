from lambdas.config.config import logger
from lambdas.config.config import CONNECTION_KEY
from lambdas.config.config import DAL_URL
from lambdas.db.connection import DbConnection
from lambdas.schema.models import Shifters, Shifts
from lambdas.utils.util import get_api_data






def save_shift(data):
    """ This function used to save shift data into database.

    Args:
    data (dict): Shift data.

    Returns:
    dict: The return value. """

    # Initialize return value
    return_value = {
        "statusCode": None,
        "body": None
    }

    try:
        # Initialize database connection
        response = DbConnection.openconnection(CONNECTION_KEY)
        if response["statusCode"] == 200:
            # Initialize shift object.
            shift = Shifts(
                id=data['shiftid'],
                shiftid=data['shiftid'],
                jobproviderid=data['jobproviderid'],
                location=[float(data['longitude']), float(data['latitude'])],
                shiftdetail=data["shiftdetail"]
            )
            # To save shift data in database.
            shift.save()
            logger.info("Saved data successfully")
            return_value["statusCode"] = 200
            return_value["body"] = "Success"
        else:
            return_value = response
    except BaseException as exceptions:
        message = str(exceptions)
        logger.error("Shift data not saved! Error: %s", message)
        return_value["statusCode"] = 500
        return_value["body"] = message
    return return_value


def save_shifter(data):
    """ This function used to save shifter data into database.

    Args:
    data (dict): Shifter data.

    Returns:
    dict: The return value. """

    # Initialize return value
    return_value = {
        "statusCode": None,
        "body": None
    }

    try:
        response = DbConnection.openconnection(CONNECTION_KEY)
        if response["statusCode"] == 200:
            # Initialize shifter object.
            shifter = Shifters(
                id=data['id'],
                shifterid=data['id'],
                existingshifterjpid=data['existingshifterjpid'],
                position=data['position'],
                location=[float(data['longitude']), float(data['latitude'])],
                rating=data['rating'],
                shifteravailability=data['shifteravailability']
            )
            # To save shifter data in database.
            shifter.save()
            logger.info("Saved data successfully")
            return_value["statusCode"] = 200
            return_value["body"] = "Success"
        else:
            return_value = response
    except BaseException as exceptions:
        message = str(exceptions)
        logger.error("Shifter data not saved! Error: %s", message)
        return_value["statusCode"] = 500
        return_value["body"] = message
    return return_value


def sqs(body):

    """ This function used to call dal api and save response into mongo db according
    to request params.

    Notes: 'This function use helper function to save shift and shifter data

    Args:
    body (dict): required for call dal api.

    Returns:
    dict: The return value. """

    # initialize return value.
    return_value = {
        "statusCode": None,
        "body": None
    }

    try:
        # Initialize request body to call dal api.
        request_body = {
            "ID": body['Id'],
            "Type": body['nType']
        }
        # To parse as string and log the request body comming from sqs.
        request_body_string = str(body)
        logger.debug("Request body from sqs %s", request_body_string)
        # To call dal api and store response in result variable.
        result = get_api_data(DAL_URL['base_url'], request_body, DAL_URL["token"])
        # To check if dal api call success.
        if result["statusCode"] == 200:
            logger.info("DAL api called success for type %s", body['nType'])
            data = result["body"].json()
            if data['data']:
                data = data['data'][0]
                logger.info("Get data from dal api succeeded")
                # To switch according to type.
                if body['nType'] == 'shifter':
                    # Call shifter function to save shifter data.
                    response = save_shifter(data)
                    return_value = response
                elif body['nType'] == 'shift':
                    # Call shift function to save shift data.
                    response = save_shift(data)
                    return_value = response
            else:
                logger.error("Response %s %s.", data["status"], data["message"])
                return_value["statusCode"] = data['status']
                return_value["body"] = data['message']
        else:
            logger.error("Error during call dal api!")
            return_value = result
    except BaseException as exceptions:
        message = str(exceptions)
        logger.error("Error ! %s", message)
        return_value['statusCode'] = 500
        return_value['body'] = message
    return return_value
