import os
import pathlib
import configparser

__file_path = os.path.abspath(__file__)
__dir_path = os.path.dirname(__file_path)

PROJ_LOC=pathlib.Path(__dir_path).parent
SQLITE_DATABASE_LOCATION=os.path.join(PROJ_LOC, "database")
SQLITE_DATABASE_NAME="user_access_tokens.db"

__app_config = configparser.ConfigParser()
__app_config.read(os.path.join(PROJ_LOC,'config.ini'))

FITBIT_CONFIG = __app_config['FITBIT']

AVRO_SCHEMA_LOC=os.path.join(PROJ_LOC, "avro")