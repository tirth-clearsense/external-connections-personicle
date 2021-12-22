from application.models.external_connections import ExternalConnections
from application.models.base import db

import requests
from datetime import datetime, timedelta
import pprint
import json

GOOGLE_FIT_SESSIONS_ENDPOINT = "https://www.googleapis.com/fitness/v1/users/me/sessions"
SLEEP_ACTIVITY = 72

SESSIONS_DATE_OFFSET = timedelta(days=7)

from application.config import GOOGLE_FIT_CONFIG
# from application import app

def google_fit_activity_import(*args, **kwargs):
    pass


def google_fit_sessions_import(personicle_user_id, google_fit_user_id, access_token, last_accessed_at, google_fit_oauth_config):
    """
    Get all sleep events and related data from google fit REST api
    Google fit sleep get endpoint: https://www.googleapis.com/fitness/v1/users/me/sessions?startTime=2019-12-05T00:00.000Z&endTime=2019-12-17T23:59:59.999Z&activityType=72
    """
    google_fit_sleep_endpoint = GOOGLE_FIT_SESSIONS_ENDPOINT.format(activity_type=SLEEP_ACTIVITY)
    start_time = datetime.utcnow() - SESSIONS_DATE_OFFSET if last_accessed_at is None else last_accessed_at
    count_sessions = 0
    while start_time <= datetime.utcnow():
        end_time = start_time + SESSIONS_DATE_OFFSET
        query_parameters = {
            "startTime": start_time.strftime("%Y-%m-%dT%H:%M:%S%zZ"),
            "endTime": end_time.strftime("%Y-%m-%dT%H:%M:%S%zZ")
            # "activityType": SLEEP_ACTIVITY
        }

        query_header = {
            "accept": "application/json",
            "authorization": "Bearer {}".format(access_token)
        }
    
        activities_response = requests.get(google_fit_sleep_endpoint, headers=query_header, params=query_parameters)
        activities = json.loads(activities_response.content)

        pprint.pprint(activities)
        # SEND DATA TO KAFKA 
        start_time = end_time
        count_sessions += len(activities['session'])
    return True, count_sessions


def google_fit_dataset_import(personicle_user_id, access_token, last_accessed_at):

    pass

def initiate_google_fit_data_import(personicle_user_id, *args, **kwargs):
    """
    Parameter:
    personicle_user_id

    Action:
    get google fit access token from sqlite db
    download user activities and data from google fit api
    send the data to kafka producer

    GOOGLE FIT ACTIVITIES ENDPOINT: 

    Returns:
    None
    """
    google_fit_oauth_config = GOOGLE_FIT_CONFIG
    # with app.app_context():
    user_credentials = ExternalConnections.query.filter_by(userId=personicle_user_id, service='google-fit').all()
    if len(user_credentials) == 0:
        return None
    assert len(user_credentials) == 1, "Duplicate google fit credentials for user: {}".format(personicle_user_id)

    # with app.app_context():
    user_record = ExternalConnections.query.filter_by(userId=personicle_user_id, service='google-fit').one()

    google_fit_user_id = user_record.external_user_id
    last_accessed_at = user_record.last_accessed_at

    google_fit_sessions_import(personicle_user_id, google_fit_user_id, user_record.access_token, last_accessed_at, google_fit_oauth_config)
    
    user_record.last_accessed_at = datetime.utcnow()
    db.session.commit()
    return True
    # get access token from sqlite
    # call api end points for different data scopes included in the request
    # these include activities, sleep, different data streams such as heart rate , steps, weight etc.

