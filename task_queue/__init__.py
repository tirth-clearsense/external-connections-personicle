from azure.storage.queue import (
        QueueService,
        QueueMessageFormat
)
import json
import os, uuid
from application.config import TASK_QUEUE_CONFIG
import logging

LOG = logging.getLogger(__name__)

connect_str_google = TASK_QUEUE_CONFIG['CONNECTION_STRING']
queue_name_google = TASK_QUEUE_CONFIG['QUEUE_NAME']
connect_str_oura = TASK_QUEUE_CONFIG['CONNECTION_STRING_OURA']
queue_name_oura = TASK_QUEUE_CONFIG['QUEUE_NAME_OURA']


def send_download_task_request(personicle_user_id, personicle_token, external_service_name, external_service_token, last_accessed_at):
    """
    Parameters:
    Personicle User id
    Personicle bearer token
    External service name
    External service access token
    last accessed timestamp
    """
    
    request_message = {
        "individual_id": personicle_user_id,
        "personicle_token": personicle_token,
        "service_name": external_service_name,
        "service_access_token": external_service_token,
        "last_accessed_at": str(last_accessed_at) if last_accessed_at else None
    }
    if external_service_name == "oura":
        queue_name = queue_name_oura
        connect_str = connect_str_oura
    elif external_service_name == "google-fit":
        queue_name = queue_name_google
        connect_str = connect_str_google

    LOG.info("Sending message to task queue {}: {}".format(queue_name, json.dumps(request_message)))
    queue_service = QueueService(connection_string=connect_str)

    queue_service.encode_function = QueueMessageFormat.text_base64encode
    # queue_service.decode_function = QueueMessageFormat.binary_base64decode

    message = json.dumps(request_message)
    print("Adding message: " + message)
    queue_service.put_message(queue_name, message)
    return


        