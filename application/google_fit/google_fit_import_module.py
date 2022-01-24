from application.models.external_connections import ExternalConnections
from application.models.base import db

import requests
from datetime import datetime, timedelta
import pprint
import json
import logging
from .utils.google_fit_datasets import get_data_sources, get_dataset_for_datasource

GOOGLE_FIT_SESSIONS_ENDPOINT = "https://www.googleapis.com/fitness/v1/users/me/sessions"
GOOGLE_FIT_DATA_SOURCES = "https://www.googleapis.com/fitness/v1/users/me/dataSources"

SLEEP_ACTIVITY = 72

SESSIONS_DATE_OFFSET = timedelta(days=7)

from application.config import GOOGLE_FIT_CONFIG
from . import google_fit_upload_azure
# from application import app

LOG = logging.getLogger(__name__)

def google_fit_sessions_import(personicle_user_id, google_fit_user_id, access_token, last_accessed_at, google_fit_oauth_config):
    """
    Get all sleep events and related data from google fit REST api
    Google fit sleep get endpoint: https://www.googleapis.com/fitness/v1/users/me/sessions?startTime=2019-12-05T00:00.000Z&endTime=2019-12-17T23:59:59.999Z&activityType=72
    """
    google_fit_sleep_endpoint = GOOGLE_FIT_SESSIONS_ENDPOINT.format(activity_type=SLEEP_ACTIVITY)
    if last_accessed_at is None:
        start_time = None
        end_time = datetime.utcnow()
    else:
        start_time = last_accessed_at
        end_time = None
    count_sessions = 0
    repeat_token = None
    call_api = True
    while call_api:
        # end_time = start_time + SESSIONS_DATE_OFFSET
        query_parameters = {}
        if start_time:
            query_parameters['startTime'] = start_time.strftime("%Y-%m-%dT%H:%M:%S%zZ")
        if end_time:
            query_parameters['endTime'] = end_time.strftime("%Y-%m-%dT%H:%M:%S%zZ")
        if repeat_token:
            query_parameters['pageToken'] = repeat_token

        query_header = {
            "accept": "application/json",
            "authorization": "Bearer {}".format(access_token)
        }

        LOG.info("Requesting google-fit data for user {} from {} to {}".format(personicle_user_id, start_time, end_time))
    
        activities_response = requests.get(google_fit_sleep_endpoint, headers=query_header, params=query_parameters)
        activities = json.loads(activities_response.content)

        LOG.info("Number of sessions: {}".format(len(activities['session'])))
        LOG.info("Received payload: {}".format(json.dumps(activities, indent=2)))
        # SEND DATA TO KAFKA 
        if len(activities['session']) > 0:
            google_fit_upload_azure.send_records_to_producer(personicle_user_id, activities['session'], 'activity')

        call_api = activities.get('hasMoreData', False)
        repeat_token = activities.get('nextPageToken', None)

        # start_time = end_time
        count_sessions += len(activities['session'])
    LOG.info("Number of sessions sent : {}".format(count_sessions))
    return True, count_sessions


def google_fit_dataset_import(personicle_user_id, access_token, last_accessed_at):
    """
    Get all datasets for the current user
    First need to list all data sources for the user
    Then download the datasets for each data source
    """
    datasources_list = get_data_sources(access_token)

    for source in datasources_list:
        # get the data type from source
        data_type = source['dataType']['name'].split(".")[-1]
        
        # map the data type to a table
        # get the data for the source
        pass
    return

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
    print("Initiating google fit data import")
    user_credentials = ExternalConnections.query.filter_by(userId=personicle_user_id, service='google-fit').all()
    if len(user_credentials) == 0:
        print("No google fit credentials found for user: {}".format(personicle_user_id))
        return None
    assert len(user_credentials) == 1, "Duplicate google fit credentials for user: {}".format(personicle_user_id)
    print("Found user access token")
    user_record = ExternalConnections.query.filter_by(userId=personicle_user_id, service='google-fit').one()

    google_fit_user_id = user_record.external_user_id
    last_accessed_at = user_record.last_accessed_at

    session_status, num_sessions = google_fit_sessions_import(personicle_user_id, google_fit_user_id, user_record.access_token, last_accessed_at, google_fit_oauth_config)
    
    datasets_added = google_fit_dataset_import(personicle_user_id, user_record.access_token, last_accessed_at)

    if num_sessions > 0:
        user_record.last_accessed_at = datetime.utcnow()
    db.session.commit()
    return True
    # get access token from sqlite
    # call api end points for different data scopes included in the request
    # these include activities, sleep, different data streams such as heart rate , steps, weight etc.

