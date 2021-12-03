import json
from producer.send_record import send_record
from .utils.fitbit_parsers import *
import os

# set Kafka listener port from config file

allowed_streams = ['heartrate', 'activity']

RECORD_PROCESSING = {
    'heartrate': format_heartrate,
    'activity': fitbit_activity_parser 
}

SCHEMA_LOC = './avro'
SCHEMA_MAPPING = {
    'heartrate': 'fitbit_stream_schema.avsc',
    'activity': 'event_schema.avsc'
}

TOPIC_MAPPING = {
    'heartrate': 'fitbit_stream_heartrate',
    'activity': 'fitbit_events_activity'
}



class Bunch(object):
    def __init__(self, adict):
        self.__dict__.update(adict)


def send_records_to_producer(personicle_user_id, records, stream_name, limit = None):
    count = 0
    record_formatter = RECORD_PROCESSING[stream_name]
    schema = SCHEMA_MAPPING[stream_name]
    topic = TOPIC_MAPPING[stream_name]
    for record in records:
        formatted_record = record_formatter(record, personicle_user_id)
        print(formatted_record)
        count += 1

        # send the record and schema to producer
        args = Bunch({
                    'topic': topic,
                    'schema_file': schema,
                    'record_value': json.dumps(formatted_record),
                    "bootstrap_servers": "localhost:9092",
                    "schema_registry": "http://localhost:8081",
                    "record_key": None
                })
        print(args.schema_file)
        send_record(args)

        if limit is not None and count <= limit:
            break


def send_records_from_file_to_producer(filename, stream_name, limit = None):
    count = 0
    record_formatter = RECORD_PROCESSING[stream_name]
    schema = SCHEMA_MAPPING[stream_name]
    topic = TOPIC_MAPPING[stream_name]

    with open(filename, "r") as record_file:
        records = json.load(record_file)

    for record in records:
        formatted_record = record_formatter(record)
        print(formatted_record)
        count += 1

        # send the record and schema to producer
        args = Bunch({
                    'topic': topic,
                    'schema_file': schema,
                    'record_value': json.dumps(formatted_record),
                    "bootstrap_servers": "localhost:9092",
                    "schema_registry": "http://localhost:8081",
                    "record_key": None
                })
        print(args.schema_file)
        send_record(args)

        if limit is not None and limit <= count:
            break

if __name__ == "__main__":
    send_records_to_producer("./pmdata/p01/fitbit/heart_rate.json", "heartrate")
    
    # Test Command
    # python send_record.py --topic test_event --schema-file quick-test-schema.avsc --record-value '{"id": 999, "product": "foo", "quantity": 100, "price": 50}'