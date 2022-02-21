from flask import Flask
# from flask import request, session, redirect
# from flask_sqlalchemy import SQLAlchemy
import os
from . import config
from logging.config import fileConfig
from flask_cors import CORS
import logging

def create_app():
    from . import models, fitbit, ios_healthkit, google_fit,okta_authenticate
    
    app = Flask(__name__)
    CORS(app)
    app.secret_key = os.urandom(24)
    # os.makedirs(config.SQLITE_DATABASE_LOCATION, exist_ok=True)

    if os.environ.get("INGESTION_PROD", '0') != '1':
        fileConfig('logging.cfg')
    else:
        fileConfig('logging.cfg')
        # TO DO: use replace file based logging with gunicorn logger 
        # gunicorn_logger = logging.getLogger('gunicorn.error')
        # app.logger.handlers = gunicorn_logger.handlers
        # app.logger.setLevel(gunicorn_logger.level)

   
    
    okta_authenticate.init_app(app)
    # Add database URI here
    # Database url format/
    # dialect+driver://username:password@host:port/database
    # e.g., postgresql+pg8000://dbuser:kx%25jj5%2Fg@pghost10/appdb
    #   if os.environ.get("INGESTION_PROD", '0') != '1':
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{username}:{password}@{dbhost}/{dbname}".format(username=os.environ['CREDENTIALS_DB_USER'], password=os.environ['CREDENTIALS_DB_PASSWORD'],
                                                                                                                dbhost=os.environ['CREDENTIALS_DB_HOST'], dbname=os.environ['CREDENTIALS_DB_NAME'])
    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(config.SQLITE_DATABASE_LOCATION, config.SQLITE_DATABASE_NAME))

    models.init_app(app)
    fitbit.init_app(app)
    ios_healthkit.init_app(app)
    google_fit.init_app(app)
    
    # services.init_app(app)
    return app

# app = create_app()