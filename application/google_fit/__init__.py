import traceback
from flask.app import Flask


def init_app(app: Flask):
    # register the models
    # create the tables
    # register blueprints
    try:
        from .google_api_routes import google_API_routes #, oauth
        app.register_blueprint(google_API_routes)
    except Exception as e:
        print(traceback.format_exc())
        raise e
    # oauth.init_app(app)
    