from models import ExternalConnections
import requests
import configparser
from datetime import datetime

FITBIT_ACTIVITIES_ENDPOINT = "/1/user/{user_id}/activities/list.json"

config = configparser.ConfigParser()
config.read('config.ini')

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
    fitbit_oauth_config = config['FITBIT']
    user_credentials = ExternalConnections.query.filter_by(userId=personicle_user_id, service='fitbit').all()
    if len(user_credentials) == 0:
        return None
    assert len(user_credentials) == 1, "Duplicate fitbit credentials for user: {}".format(personicle_user_id)

    user_record = ExternalConnections.query.filter_by(userId=personicle_user_id, service='fitbit').one()

    fitbit_user_id = user_record.external_user_id
    activities_api_endpoint = fitbit_oauth_config['API_ENDPOINT'] + FITBIT_ACTIVITIES_ENDPOINT.format(user_id=fitbit_user_id)

    if user_record.last_accessed_at is None:
        query_parameters = {
            'beforeDate': datetime.date(datetime.utcnow()),
            'sort': 'desc'
        }
    else:
        query_parameters = {
            'afterDate': user_record.last_accessed_at,
            'sort': 'asc'
        }

    query_header = {
        "accept": "application/json",
        "authorization": "Bearer {}".format(user_record.access_token)
    }
   
    activities_response = requests.get(activities_api_endpoint, headers=query_header, params=query_parameters)
    activities = activities_response.content

    print(activities)
    return


IMPORT_MODULES = {
    'fitbit': initiate_fitbit_data_import
}

if __name__ == "__main__":
    initiate_fitbit_data_import("test_id")