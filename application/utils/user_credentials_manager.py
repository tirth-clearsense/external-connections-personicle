from datetime import datetime, timedelta
from application.models.external_connections import ExternalConnections

def add_access_token(personicle_user_id, **kwargs):
    """
    Add an access token for importing user data from external server (e.g. Fitbit)

    Parameters:
    required:
    personicle_user_id: User id for the user in personicle servers
    service_name: Name of the external service
    access_token: Access token value
    expires_in: Time before expiration for the token
    created_at: Time of token creation

    Optional arguments:
    external_user_id: user id for the external API service (e.g. fitbit user id)
    refresh_token: Refresh token value
    """
    required_arguments = ["service_name", "access_token", "expires_in", "created_at"]
    optional_arguments = ["external_user_id", "refresh_token"]

    for i in required_arguments:
        assert i in kwargs, "Missing required parameter: {}".format(i)

    new_record = ExternalConnections(userId=personicle_user_id, service=kwargs['service_name'], access_token=kwargs['access_token'], expires_in=kwargs['expires_in'],
                                        created_at=kwargs['created_at'], external_user_id=kwargs.get('external_user_id', None), refresh_token=kwargs.get("refresh_token", None))
    # check if user already exists
    user_records = ExternalConnections.query.filter_by(userId=personicle_user_id, service=kwargs['service_name']).all()
    if len(user_records) > 0:
    # Update the user record
        assert len(user_records) == 1, "Duplicate records {} found for user: {}".format(kwargs['service_name'], personicle_user_id)
        user_record = ExternalConnections.query.filter_by(userId=personicle_user_id, service=kwargs['service_name']).one()
        user_record.access_token = kwargs['access_token']
        user_record.expires_in = kwargs['expires_in']
        user_record.created_at = kwargs['created_at']

        user_record.refresh_token = kwargs.get("refresh_token", None)
        user_record.external_user_id = kwargs.get("external_user_id", None)
        user_record.scope = kwargs.get("scope", None)

        return "update", user_record
    else:
    # Add the user record
        return "add", new_record
    # return the record and add it in the calling method


def verify_user_connection(personicle_user_id, connection_name):
    """
    Return True if the user has an active access token for the requested service, if not then request a new access token
    """
    # check if user already exists
    user_records = ExternalConnections.query.filter_by(userId=personicle_user_id, service=connection_name).all()
    if len(user_records) > 0:
        assert len(user_records) == 1, "Duplicate records {} found for user: {}".format(connection_name, personicle_user_id)
        user_record = ExternalConnections.query.filter_by(userId=personicle_user_id, service=connection_name).one()
        time_created = user_record.created_at
        life_time = user_record.expires_in
        print("Time of creation: {}".format(time_created))
        print("Expires_in: {}".format(life_time))

        if datetime.utcnow() >= time_created+timedelta(seconds=life_time):
            return False
        else:
            return True
        
    else:
        return False