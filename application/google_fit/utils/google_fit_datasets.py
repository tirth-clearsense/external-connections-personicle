import json
import requests
import logging

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

    LOG.info("Number of sources: {}".format(len(data_sources['dataSource'])))
    LOG.info("Received payload: {}".format(json.dumps(data_sources, indent=2)))

    return data_sources

def get_dataset_for_datasource(access_token, datasource, dataset_id):
    """
    Get the dataset associated with a data source and the dataset id
    params:
    access_token: string, Oauth2.0 access token
    datasource: string, Google fit data source obtained from "get_data_sources" method
    dataset_id: string, gives the time range for the dataset, {start_time}-{end_time}, timestamps in nanoseconds
    """
    query_header = {
        "accept": "application/json",
        "authorization": "Bearer {}".format(access_token)
    }

    
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

        LOG.info("Number of data points: {}".format(len(dataset['point'])))
        LOG.info("Received payload: {}".format(json.dumps(dataset, indent=2)))

        # map dataset to table and event hub topic

        # send data to event hub topic
    return