from datetime import datetime, timedelta
import pytz
import json

def google_activity_parser(raw_event, personicle_user_id):
    """
    Format an activity received from google fit API to personicle event schema
    """
    new_event_record = {}
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=None)
    new_event_record['individual_id'] = personicle_user_id
    # timestamp format 2021-11-25T09:27:30.000-08:00
    new_event_record['start_time'] = int(raw_event['startTimeMillis'])
    duration = int(raw_event['startTimeMillis']) - int(raw_event['endTimeMillis'])
    new_event_record['end_time'] = int(raw_event['endTimeMillis'])

    new_event_record['event_name'] = raw_event['name']
    new_event_record['source'] = 'google-fit'
    new_event_record['parameters'] = json.dumps({
        "duration": duration,
        "source_device": raw_event['application']
    })
    return new_event_record

def google_sleep_parser(raw_event, personicle_user_id):
    pass

def google_datastream_parser(raw_records, stream_name, personicle_user_id):
    pass

