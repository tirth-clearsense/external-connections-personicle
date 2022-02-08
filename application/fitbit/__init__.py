
from flask.app import Flask
from okta import UsersClient
from flask_oidc import OpenIDConnect

def init_app(app: Flask):
    # register the models
    # create the tables
    # register blueprints

    from .authorization_routes import fitbit_routes
    app.register_blueprint(fitbit_routes)
    