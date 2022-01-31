from os import stat
from application.models.external_connections import ExternalConnections
import requests
from datetime import datetime
import pprint
import json
import logging

from . import fitbit_upload

FITBIT_ACTIVITIES_ENDPOINT = "/1/user/{user_id}/activities/list.json"

FITBIT_SLEEP_LOG_ENDPOINT = "/1.2/user/{user_id}/sleep/list.json"

from application.config import FITBIT_CONFIG
# from application import app

LOG = logging.getLogger(__name__)

def fitbit_activity_import(personicle_user_id, fitbit_user_id, access_token, last_accessed_at, fitbit_oauth_config):
    activities_api_endpoint = fitbit_oauth_config['API_ENDPOINT'] + FITBIT_ACTIVITIES_ENDPOINT.format(user_id=fitbit_user_id)

    if last_accessed_at is None:
        query_parameters = {
            'beforeDate': datetime.date(datetime.utcnow()),
            'sort': 'desc',
            'offset': 0,
            'limit': 100
        }
    else:
        query_parameters = {
            'afterDate': last_accessed_at,
            'sort': 'asc',
            'offset': 0,
            'limit': 100
        }

    query_header = {
        "accept": "application/json",
        "authorization": "Bearer {}".format(access_token)
    }
    LOG.info("Requesting fitbit activities with query parameters: {}".format(query_parameters))
    activities_response = requests.get(activities_api_endpoint, headers=query_header, params=query_parameters)
    activities = json.loads(activities_response.content)

    LOG.info("Received payload: {}".format(json.dumps(activities, indent=2)))
    if 'activities' not in activities:
        LOG.error("Incorrect response received")
        return False, activities
    
    # Parse every event, send to producer and update the last accessed\
    fitbit_upload.send_records_to_producer(personicle_user_id, activities['activities'], 'activity')

    # CHECK FOR PAGINATED RESPONSE

    return True, len(activities['activities'])

def fitbit_sleep_import(personicle_user_id, fitbit_user_id, access_token, last_accessed_at, fitbit_oauth_config):
    sleep_api_endpoint = fitbit_oauth_config['API_ENDPOINT'] + FITBIT_SLEEP_LOG_ENDPOINT.format(user_id=fitbit_user_id)

    if last_accessed_at is None:
        query_parameters = {
            'beforeDate': datetime.date(datetime.utcnow()),
            'sort': 'desc',
            'offset': 0,
            'limit': 100
        }
    else:
        query_parameters = {
            'afterDate': last_accessed_at,
            'sort': 'asc',
            'offset': 0,
            'limit': 100
        }

    query_header = {
        "accept": "application/json",
        "authorization": "Bearer {}".format(access_token)
    }
    LOG.info("Requesting fitbit sleep events with query parameters: {}".format(query_parameters))
    sleep_response = requests.get(sleep_api_endpoint, headers=query_header, params=query_parameters)
    sleep = json.loads(sleep_response.content)

    LOG.info("Received payload: {}".format(json.dumps(sleep, indent=2)))
    if 'sleep' not in sleep:
        LOG.error("Incorrect response received")
        return False, sleep

    # Parse every event, send to producer and update the last accessed\
    fitbit_upload.send_records_to_producer(personicle_user_id, sleep['sleep'], 'sleep')
    # CHECK FOR PAGINATED RESPONSE

    return True, len(sleep['sleep'])

def fitbit_intraday_heartrate_import():
    pass

def fitbit_intraday_steps_import():
    pass

def initiate_fitbit_data_import(personicle_user_id):
    """
    Description:
    Get user data from fitbit REST API
    Activities, sleep, intra day step count and heart rate, body weight and body fat
    
    Activities also have associated tcx file that contain detailed performance metrics during the activity

    Parameter:
    personicle_user_id

    Action:
    get fitbit access token from sqlite db
    download user activities and data from fitbit api
    send the data to kafka producer

    FITBIT ACTIVITIES ENDPOINT: /1/user/[user-id]/activities/list.json

    Returns:
    None
    """
    fitbit_oauth_config = FITBIT_CONFIG
    # with app.app_context():
    user_credentials = ExternalConnections.query.filter_by(userId=personicle_user_id, service='fitbit').all()
    if len(user_credentials) == 0:
        return None
    assert len(user_credentials) == 1, "Duplicate fitbit credentials for user: {}".format(personicle_user_id)

    # with app.app_context():
    user_record = ExternalConnections.query.filter_by(userId=personicle_user_id, service='fitbit').one()

    fitbit_user_id = user_record.external_user_id
    last_accessed_at = user_record.last_accessed_at

    status, activities_response = fitbit_activity_import(personicle_user_id, fitbit_user_id, user_record.access_token, last_accessed_at, fitbit_oauth_config)
    
    response = {"activity_success": status, "activities_response": activities_response}
    return status, response


IMPORT_MODULES = {
    'fitbit': initiate_fitbit_data_import
}

if __name__ == "__main__":
    initiate_fitbit_data_import("test_id")