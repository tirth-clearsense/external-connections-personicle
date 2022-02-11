from flask import Flask
# from flask import request, session, redirect
# from flask_sqlalchemy import SQLAlchemy
import os
from . import config
from logging.config import fileConfig
from flask_cors import CORS

def create_app():
    from . import models, fitbit, ios_healthkit, google_fit,okta_authenticate
    
    app = Flask(__name__)
    CORS(app)
    app.secret_key = os.urandom(24)
    os.makedirs(config.SQLITE_DATABASE_LOCATION, exist_ok=True)

    fileConfig('logging.cfg')

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(config.SQLITE_DATABASE_LOCATION, config.SQLITE_DATABASE_NAME))
    
    okta_authenticate.init_app(app)
    models.init_app(app)
    fitbit.init_app(app)
    ios_healthkit.init_app(app)
    google_fit.init_app(app)
    
    # services.init_app(app)
    return app

# app = create_app()