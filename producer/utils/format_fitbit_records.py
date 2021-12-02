from datetime import datetime

def format_heartrate(raw_record, individual_id = 'p01'):
    new_record = {}
    epoch = datetime.utcfromtimestamp(0)
    new_record['individual_id'] = individual_id
    new_record['timestamp'] = (datetime.strptime(raw_record['dateTime'], "%Y-%m-%d %H:%M:%S") - epoch).total_seconds()*1000
    new_record['stream'] = 'heartrate'
    new_record['value'] = raw_record['value']['bpm']
    new_record['unit'] = 'bpm'
    new_record['confidence'] = raw_record['value']['confidence']

    return new_record


def format_events(raw_event, individual_id='p01'):
    new_event_record = {}
    epoch = datetime.utcfromtimestamp(0)
    new_event_record['individual_id'] = individual_id
    # 2021-11-25T09:27:30.000-08:00
    new_event_record['start_timestamp'] = (datetime.strptime(raw_event['startTime'], "%Y-%m-%dT%H:%M:%S.%f"))
    duration = raw_event
