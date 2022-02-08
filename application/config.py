import os
import pathlib
import configparser

__file_path = os.path.abspath(__file__)
__dir_path = os.path.dirname(__file_path)

PROJ_LOC=pathlib.Path(__dir_path).parent
AVRO_SCHEMA_LOC=os.path.join(PROJ_LOC, "avro")

# Database url format
# dialect+driver://username:password@host:port/database
# postgresql+pg8000://dbuser:kx%25jj5%2Fg@pghost10/appdb

if os.environ.get("INGESTION_PROD", 0) != 1:
    SQLITE_DATABASE_LOCATION=os.path.join(PROJ_LOC, "database")
    SQLITE_DATABASE_NAME="user_access_tokens.db"

    __app_config = configparser.ConfigParser()
    __app_config.read(os.path.join(PROJ_LOC,'config.ini'))

    HOST_CONFIG = __app_config['HOST']
    FITBIT_CONFIG = __app_config['FITBIT']
    IOS_APP_CONFIG = __app_config['IOS_APP']
    GOOGLE_FIT_CONFIG = __app_config['GOOGLE_FIT']

    KAFKA_CONFIG = __app_config['KAFKA']

    EVENTHUB_CONFIG = __app_config['EVENTHUB']

    DB_CONFIG = __app_config['CREDENTIALS_DATABASE']

    os.environ['CREDENTIALS_DB_USER'] = DB_CONFIG['USERNAME']
    os.environ['CREDENTIALS_DB_PASSWORD'] = DB_CONFIG['PASSWORD']
    os.environ['CREDENTIALS_DB_HOST'] = DB_CONFIG['HOST']
    os.environ['CREDENTIALS_DB_NAME'] = DB_CONFIG['NAME']
else:
    HOST_CONFIG = {
        'HOST_ADDRESS': os.environ['HOST_ADDRESS']
    }

    FITBIT_CONFIG = {
        'CLIENT_ID': os.environ['FITBITCLIENTID'],
        'CLIENT_SECRET': os.environ['FITBITCLIENTSECRET'],
        'REDIRECT_URL': os.environ['FITBITREDIRECTURL'],
        'AUTH_URL': os.environ['FITBITAUTHURL'],
        'REQUEST_URL': os.environ['FITBITREQUESTURL'],
        'API_ENDPOINT': os.environ['FITBITAPIENDPOINT']
    }

    GOOGLE_FIT_CONFIG = {
        'CLIENT_ID': os.environ['GOOGLEFITCLIENTID'],
        'CLIENT_SECRET': os.environ['GOOGLEFITCLIENTSECRET'],
        'REDIRECT_URL': os.environ['GOOGLEFITREDIRECTURL'],
        'AUTH_URL': os.environ['GOOGLEFITAUTHURL'],
        'API_ENDPOINT': os.environ['GOOGLEFITAPIENDPOINT'],
        'TOKEN_URL': os.environ['GOOGLEFITTOKENURL'],
        'SECRET_JSON': os.environ['GOOGLEFITSECRETJSON']
    }

    IOS_APP_CONFIG = {
        'KEY': os.environ['IOS_APP_KEY']
    }

    EVENTHUB_CONFIG = {
        'CONNECTION_STRING': os.environ['EVENTHUB_CONNECTION_STRING'],
        'EVENTHUB_NAME': os.environ['EVENTHUB_NAME'],
        'SCHEMA_REGISTRY_FQNS': os.environ['EVENTHUB_SCHEMA_REGISTRY_FQNS'],
        'SCHEMA_REGISTRY_GROUP': os.environ['EVENTHUB_SCHEMA_REGISTRY_GROUP']
    }
