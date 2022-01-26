import json
from producer.send_record import send_record
from producer.send_records_azure import send_records_to_eventhub

from .utils.healthkit_parsers import *
import os
import logging

LOG = logging.getLogger(__name__)


# set Kafka listener port from config file

allowed_streams = ['sleep']

RECORD_PROCESSING = {
    'sleep': format_healthkit_sleep_event
}

SCHEMA_LOC = './avro'
SCHEMA_MAPPING = {
    'sleep': 'event_schema.avsc'
}

TOPIC_MAPPING = {
    'sleep': 'healthkit_events_sleep'
}



class Bunch(object):
    def __init__(self, adict):
        self.__dict__.update(adict)


def send_records_to_producer(personicle_user_id, records, stream_name, limit = None):
    count = 0
    record_formatter = RECORD_PROCESSING[stream_name]
    schema = SCHEMA_MAPPING[stream_name]
    topic = TOPIC_MAPPING[stream_name]


    LOG.info("Sending records to producer")
    LOG.info("Formatting records...")
    for record in records:

        formatted_record = record_formatter(record, personicle_user_id)
        count += 1

        # # send the record and schema to producer
        # args = Bunch({
        #             'topic': topic,
        #             'schema_file': schema,
        #             'record_value': json.dumps(formatted_record),
        #             "bootstrap_servers": "localhost:9092",
        #             "schema_registry": "http://localhost:8081",
        #             "record_key": None
        #         })
        # print(args.schema_file)

        # send_record(args)

        if count == 0:
            LOG.info("Calling send_records_to_eventhub...")
            LOG.info(str(formatted_record))

        send_records_to_eventhub(schema, formatted_record, 'testhub-new')

        if limit is not None and count <= limit:
            break



if __name__ == "__main__":
    send_records_to_producer("./heartrate.json", "heartrate")

    # Test Command
    # python send_record.py --topic test_event --schema-file quick-test-schema.avsc --record-value '{"id": 999, "product": "foo", "quantity": 100, "price": 50}'