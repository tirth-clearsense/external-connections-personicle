from flask import Flask
import os
import configparser

def create_app():
    from . import models, routes, services
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(sqlite_config['DATABASE_LOCATION'], sqlite_config['DATABASE_NAME']))

    config = configparser.ConfigParser()
    config.read('config.ini')
    
    sqlite_config = config['SQLITE']

    os.makedirs(os.path.join(sqlite_config['DATABASE_LOCATION']), exist_ok=True)

    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(sqlite_config['DATABASE_LOCATION'], sqlite_config['DATABASE_NAME']))

    models.init_app(app)
    routes.init_app(app)
    # services.init_app(app)
    return app