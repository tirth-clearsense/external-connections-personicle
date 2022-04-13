
import traceback
from flask.app import Flask


def init_app(app: Flask):
    # register the models
    # create the tables
    # register blueprints
    try:
        from .data_import_routes import healthkit_routes
        app.register_blueprint(healthkit_routes)
    except Exception as e:
        print(traceback.format_exc())
        raise e
