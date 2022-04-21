
import traceback
from flask.app import Flask
from okta import UsersClient

def init_app(app: Flask):
    # register the models
    # create the tables
    # register blueprints
    try:
        from .oura_api_routes import oura_routes
        app.register_blueprint(oura_routes)
    except Exception as e:
        print(traceback.format_exc()) 
        raise e   