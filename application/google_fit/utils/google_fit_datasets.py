import json
import requests
import logging
from data_dictionary import find_datastream
from avro_modules import validate_datastream_schema
from .google_fit_parsers import google_datastream_parser

LOG = logging.getLogger(__name__)
DATA_SOURCE_URL = "https://www.googleapis.com/fitness/v1/users/me/dataSources"
GOOGLE_FIT_DATA_SET = "https://www.googleapis.com/fitness/v1/users/me/dataSources/{dataSourceId}/datasets/{datasetId}"


def get_data_sources(access_token, data_types = None):
    """
    Get the list of datasources associated with the google fit account
    params:
    access_token: access token granted by the user via OAuth2.0
    data_types (optional): data types to be downloaded from google fit
    """

    query_header = {
        "accept": "application/json",
        "authorization": "Bearer {}".format(access_token)
    }

    if data_types is None:
        LOG.info("Querying for all data sources")
        data_sources_response = requests.get(DATA_SOURCE_URL, headers=query_header)
    else:
        LOG.info("Querying sources for following data types: {}".format(','.join(data_types)))
        data_sources_response = requests.get(DATA_SOURCE_URL, headers=query_header, params={"dataTypeName": data_types})
    data_sources = json.loads(data_sources_response.content)

    LOG.info("Received payload: {}".format(json.dumps(data_sources, indent=2)))
    LOG.info("Number of sources: {}".format(len(data_sources['dataSource'])))

    return data_sources['dataSource']

def get_dataset_for_datasource(access_token, datasource, dataset_id, personicle_data_type, personicle_user_id):
    """
    Get the dataset associated with a data source and the dataset id
    params:
    access_token: string, Oauth2.0 access token
    datasource: string, Google fit data source obtained from "get_data_sources" method
    dataset_id: string, gives the time range for the dataset, {start_time}-{end_time}, timestamps in nanoseconds
    personicle_data_type: data type for the dataset from the personicle data dictionary, for eg, com.personicle.individual.datastreams.heartrate
    personicle_user_id: id for the user in personicle ecosystem
    """
    query_header = {
        "accept": "application/json",
        "authorization": "Bearer {}".format(access_token)
    }

    total_data_points = 0
    LOG.info("Querying source: {} for time range: {}".format(datasource, dataset_id))
    next_page_token = None
    next_page = True

    while next_page:
        query_parameters = {}
        if next_page_token:
            query_parameters['pageToken'] = next_page_token

        query_header = {
            "accept": "application/json",
            "authorization": "Bearer {}".format(access_token)
        }

        LOG.info("Requesting google-fit data {} for Time range {}".format(datasource, dataset_id))

        dataset_response = requests.get(GOOGLE_FIT_DATA_SET.format(dataSourceId=datasource, datasetId=dataset_id), 
                                    headers=query_header, params=query_parameters)
        dataset = json.loads(dataset_response.content)

        LOG.info("Received payload: {}".format(json.dumps(dataset, indent=2)))
        # if the API call throws an error
        if 'error' in dataset.keys():
            LOG.error(dataset['error'])
            continue

        if 'point' not in dataset.keys():
            LOG.error("Unknown response received: {}".format(dataset))
            continue
    
        LOG.info("Number of data points: {}".format(len(dataset['point'])))

        # IN PROGRESS
        # find personicle data dictionary for the dataset
        personicle_data_description = find_datastream(personicle_data_type)
        if personicle_data_description is None:
            LOG.warn("Data type {} not present in personicel data dictionary".format(personicle_data_type))
            return total_data_points

        # format the records to match the avro schema
        formatted_records = google_datastream_parser(dataset, personicle_data_type, personicle_data_description, personicle_user_id)
        LOG.info("Formatted records: {}".format(formatted_records))
        # validate if the data points match the avro schema
        if formatted_records is None:
            LOG.info("Total data points added for source {}: {}".format(datasource, total_data_points))
            return total_data_points
            
        validated_records = validate_datastream_schema(formatted_records, personicle_data_description['base_schema'])
        if validated_records is None:
            LOG.info("Total data points added for source {}: {}".format(datasource, total_data_points))
            LOG.error("formatted records do not match the specified schema: {} \nRecords: {}".format(personicle_data_description["base_schema"], json.dumps(formatted_records, indent=2)))
            return total_data_points
        total_data_points += len(dataset['point'])

        # send data to event hub topic

        # get next page token
        next_page_token = dataset.get('nextPageToken', None)
        if next_page_token:
            next_page = True
            LOG.info("Next page token found")
        else:
            next_page = False
    LOG.info("Total data points added for source {}: {}".format(datasource, total_data_points))
    return total_data_points