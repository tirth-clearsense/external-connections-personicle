import json
from application.fitbit.fitbit_upload import RECORD_PROCESSING
# from producer.send_record import send_record
from producer.send_records_azure import send_records_to_eventhub

from .utils.google_fit_parsers import *

RECORD_PROCESSING = {
    'activity': google_activity_parser,
    'sleep': google_sleep_parser,
    'datastream': google_datastream_parser
}

SCHEMA_LOC = './avro'
SCHEMA_MAPPING = {
    'heartrate': 'fitbit_stream_schema.avsc',
    'activity': 'event_schema.avsc',
    'sleep': 'event_schema.avsc'
    }

TOPIC_MAPPING = {
    'heartrate': 'google_stream_heartrate',
    'activity': 'testhub-new',
    'sleep': 'testhub-new'
}

def send_records_to_producer(personicle_user_id, records, stream_name, limit = None):
    count = 0
    record_formatter = RECORD_PROCESSING[stream_name]
    schema = SCHEMA_MAPPING[stream_name]
    topic = TOPIC_MAPPING[stream_name]
    formatted_records = []
    for record in records:
        formatted_record = record_formatter(record, personicle_user_id)
        formatted_records.append(formatted_record)
        print(formatted_record)
        count += 1        

        if limit is not None and count <= limit:
            break
    send_records_to_eventhub("event_schema.avsc", formatted_records, "testhub-new")

