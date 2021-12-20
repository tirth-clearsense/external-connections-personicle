from application.models.external_connections import ExternalConnections
import requests
from datetime import datetime
import pprint
import json

FITBIT_ACTIVITIES_ENDPOINT = "/1/user/{user_id}/activities/list.json"

from application.config import FITBIT_CONFIG
# from application import app

def google_fit_data_import(personicle_user_id, *args, **kwargs):
    # get access token from sqlite
    # call api end points for different data scopes included in the request
    # these include activities, sleep, different data streams such as heart rate , steps, weight etc.
    pass
