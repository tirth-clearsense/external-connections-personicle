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

