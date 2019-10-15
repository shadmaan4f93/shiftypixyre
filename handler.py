import json
from lambdas.config.config import logger
from lambdas.dal.sqs import sqs
from lambdas.re.recommendation import recommendations


def dal_handler(event, context):
    """ This function use to handle post request from sqs trigger.

    Args:
        body (json): Required 'nType', 'Id'

        Returns:
        json: The return value. """

    logger.debug("Received new event: %s", repr(event))
    # Initialize response object.
    response = {
        'statusCode': None,
        'headers': {'Content-Type': 'application/json'},
        'body': str(context)
    }
    logger.info("dal_handler called seccess")
    # Get request body.
    if "body" in event:
        body = event['body']
    else:
        body = event['Records'][0]['body']
    body = json.loads(body)
    # Check if Type and ID exist in request body.
    if 'nType' in body and 'Id' in body:
        logger.info("Get nType, Id successfully")
        result = sqs(body)
        response['statusCode'] = result['statusCode']
        response['body'] = result['body']
    else:
        logger.info("Bad request formate")
        response['body'] = "Can't get 'nType' and 'Id' from request body!"
        response['statusCode'] = 400
    logger.debug("Lambda Response: %s", repr(response))
    return response


def re_handler(event, context):
    """ This handler function return recommendation acording to vacated shift, shifter parameter.

        Args:
        event["body"] (dict): request body to get recommendation.

        Returns:
        json: The return value. """

    logger.debug("Received new event: %s", repr(event))
    response = {
        'statusCode': None,
        'headers': {'Content-Type': 'application/json'},
        'body': str(context) + str(event)
    }
    vacated_params = event['body']
    if vacated_params:
        vacated_params = json.loads(vacated_params)
        result = recommendations(vacated_params)
        response['statusCode'] = result['statusCode']
        response['body'] = json.dumps(result)
    else:
        response['body'] = "Unprocessable Entity"
        response['statusCode'] = 422
        logger.error("Unable to parse request paramaters")
    logger.debug("Lambda Response: %s", repr(response))
    return response
