
from flask.app import Flask

def init_app(app: Flask):

    from .authorization_routes import okta_routes
    app.register_blueprint(okta_routes)
    