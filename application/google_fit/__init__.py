from flask.app import Flask


def init_app(app: Flask):
    # register the models
    # create the tables
    # register blueprints
    from .google_api_routes import google_API_routes #, oauth
    app.register_blueprint(google_API_routes)
    # oauth.init_app(app)
    