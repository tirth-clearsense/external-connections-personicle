
from flask.app import Flask


def init_app(app: Flask):
    # register the models
    # create the tables
    # register blueprints
    from .data_import_routes import healthkit_routes
    app.register_blueprint(healthkit_routes)
