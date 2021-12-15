from datetime import datetime, timedelta
import pytz
import json

def fitbit_activity_parser(raw_event, personicle_user_id):
    """
    Formats an activity received from FitbitAPI to personicle event schema
    """
    new_event_record = {}
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=None)
    new_event_record['individual_id'] = personicle_user_id
    # timestamp format 2021-11-25T09:27:30.000-08:00
    new_event_record['start_time'] = int((datetime.strptime(raw_event['startTime'], "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(pytz.utc).replace(tzinfo=None)-epoch).total_seconds()*1000)
    duration = timedelta(seconds=raw_event['originalDuration']/1000)
    new_event_record['end_time'] = int(new_event_record['start_time'] + duration.total_seconds()*1000)

    new_event_record['event_name'] = "activity"
    new_event_record['source'] = 'fitbit'
    new_event_record['parameters'] = json.dumps({
        "duration": duration.total_seconds(),
        "caloriesBurned": raw_event['calories'],
        'activityName': raw_event['activityName'],
        'distance': raw_event['distance'],
        'distanceUnit': raw_event['distanceUnit'],
        "activityLevel": raw_event['activityLevel']
    })
    return new_event_record
    

def format_heartrate(raw_record, personicle_user_id = 'p01'):
    new_record = {}
    epoch = datetime.utcfromtimestamp(0)
    new_record['individual_id'] = personicle_user_id
    new_record['timestamp'] = (datetime.strptime(raw_record['dateTime'], "%Y-%m-%d %H:%M:%S") - epoch).total_seconds()*1000
    new_record['stream'] = 'heartrate'
    new_record['value'] = raw_record['value']['bpm']
    new_record['unit'] = 'bpm'
    new_record['confidence'] = raw_record['value']['confidence']

    return new_record