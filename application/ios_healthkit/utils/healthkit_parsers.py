from datetime import datetime, timedelta
import pytz
import json
import logging
LOG = logging.getLogger(__name__)

def get_value_wrapper(json_obj, key, defaultvalue):
    return json_obj[key] if key in json_obj else defaultvalue

def format_healthkit_sleep_event(raw_event, personicle_user_id):
    """
    Formats a sleep event received from iOS to personicle event schema
    """
    new_event_record = {}
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=None)
    new_event_record['individual_id'] = personicle_user_id
    # timestamp format 2021-11-25T09:27:30.000-08:00

    new_event_record['start_time'] = raw_event['startTime']
    new_event_record['end_time'] = raw_event['endTime']

    new_event_record['event_name'] = "sleep"
    new_event_record['source'] = 'healthkit'
    new_event_record['parameters'] = json.dumps({
        "duration": new_event_record['end_time'] - new_event_record['start_time'],
        'device_manufacturer_name': get_value_wrapper(raw_event, 'HKDeviceManufacturerName', 'Undefined'),
        'device_name': get_value_wrapper(raw_event, 'HKDeviceName', 'Undefined'),
        'sleep_stage': get_value_wrapper(raw_event, 'SleepStage', 'Undefined'),
        'time_zone': get_value_wrapper(raw_event, 'HKTimeZone', 'Undefined')
    })

    return new_event_record
