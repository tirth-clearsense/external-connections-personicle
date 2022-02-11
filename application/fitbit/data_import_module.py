from application.models.external_connections import ExternalConnections
import requests
from datetime import datetime
import pprint
import json

from . import fitbit_upload

FITBIT_ACTIVITIES_ENDPOINT = "/1/user/{user_id}/activities/list.json"

from application.config import FITBIT_CONFIG
# from application import app

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
   
    activities_response = requests.get(activities_api_endpoint, headers=query_header, params=query_parameters)
    activities = json.loads(activities_response.content)

    pprint.pprint(activities)
    # records = []
    # for activity in activities['activities']:
    #     formatted_record = fitbit_activity_parser(activity, personicle_user_id)
    #     records.append(formatted_record)
        # send to producer
    # Parse every event, send to producer and update the last accessed\
    fitbit_upload.send_records_to_producer(personicle_user_id, activities['activities'], 'activity')
  
    return True

def fitbit_sleep_import():
    pass

def fitbit_intraday_data_import():
    pass

def initiate_fitbit_data_import(personicle_user_id):
    """
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
    # print("Reached here")
    fitbit_activity_import(personicle_user_id, fitbit_user_id, user_record.access_token, last_accessed_at, fitbit_oauth_config)
    
    return


IMPORT_MODULES = {
    'fitbit': initiate_fitbit_data_import
}

if __name__ == "__main__":
    initiate_fitbit_data_import("test_id")