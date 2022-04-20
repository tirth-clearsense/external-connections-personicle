import time
import traceback
from flask import Response, jsonify

from application.models.external_connections import ExternalConnections
from application.models.base import db
from application.config import OURA_CONFIG, HOST_CONFIG
from task_queue import send_download_task_request
import requests
from datetime import datetime, timedelta
import pprint
import json
import logging

LOG = logging.getLogger(__name__)

def initiate_oura_data_import(personicle_user_id, personicle_token, *args, **kwargs):
    LOG.info("Initiating oura import")
    user_credentials = ExternalConnections.query.filter_by(userId=personicle_user_id, service='oura').all()
    if len(user_credentials) == 0:
        print("No oura credentials found for user: {}".format(personicle_user_id))
        return None
    assert len(user_credentials) == 1, "Duplicate oura credentials for user: {}".format(personicle_user_id)
    LOG.info("Found user access token")

    user_record = ExternalConnections.query.filter_by(userId=personicle_user_id, service='oura').one()
    
    last_accessed_at = user_record.last_accessed_at
    # print(last_accessed_at)
    try:
        print("add download request to task queue")
        send_download_task_request(personicle_user_id, personicle_token, "oura", user_record.access_token, last_accessed_at)
    except Exception as e:
        LOG.error("Error while sending download request")
        LOG.error(e)

        return {"success": False, "message": "Error while sending data download request"}

    return {"success": True, "message": "Successfully created download request for oura"}