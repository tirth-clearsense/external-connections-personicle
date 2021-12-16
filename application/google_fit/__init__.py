from flask.app import Flask


def init_app(app: Flask):
    # register the models
    # create the tables
    # register blueprints
    from .authorization_routes import google_fit_routes, oauth
    app.register_blueprint(google_fit_routes)
    oauth.init_app(app)
    